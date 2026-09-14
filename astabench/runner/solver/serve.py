"""헤드리스 solve 서비스 — 외부 평가 하네스(AstaBench `agent-eval`/inspect)가 Neutropic 코어를 문항 단위로 부른다.

    python -m app.benchmarks.serve --port 8765 [--policy full] [--provider gemini]

    POST /solve  {"question": "...", "policy": "full"?, "skills": [...]?, "overrides": {...}?, "session_title": "..."?}
      → {"answer", "report_md", "documents": [{name, content}], "usage", "cost_usd", "elapsed_s", "error", "session_id"}
    GET  /health → {"ok": true, "policy": ..., "provider": ...}

전략 §14 그대로: 프로덕션 코어를 바꾸지 않는다 — 하네스 쪽 솔버가 문항을 프롬프트로 정규화해 보내고, 답변 텍스트를 하네스의
채점기가 읽는다(예: LitQA2 는 `{"answer": "<letter>"}`). 인증은 러너와 같은 평가 계정(`NEUTROPIC_EVAL_*`), 40분마다 재발급.
문항은 순차 처리(외부 DB rate-limit 페이싱 — 하네스의 max_connections=1 권장). 컨테이너: `scripts/bench-docker.sh` 에
`BENCH_DOCKER_ARGS="-p 8765:8765"` 를 얹는다(`scripts/bench-detached.py --serve`).
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Neutropic headless solve service (benchmark harness adapter)")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--policy", default="full")
    ap.add_argument("--provider", default="gemini")
    ap.add_argument("--model", default=None)
    args = ap.parse_args(argv)

    from .. import context, db
    from ..agent import policy as policy_mod
    from ..agent.headless import run_headless
    from ..providers import build_provider
    from . import perf as _perf
    from .runner import _authenticate, _needs_reauth

    preset = policy_mod.PRESETS.get(args.policy)
    if preset is None:
        raise SystemExit(f"unknown policy '{args.policy}'")
    # 하네스 문항은 되물을 사용자가 없고 프로젝트 기억은 문항 간 오염 통로다(러너 어댑터들과 같은 정규화).
    base_pol = preset.merged(approvals=False, clarify_rounds=0, project_memory=False, notebook=False, recall=False)

    state = {"caller": _authenticate(), "auth_at": time.monotonic()}
    lock = threading.Lock()   # 문항 순차 처리

    def solve(body: dict) -> dict:
        with lock:
            if _needs_reauth(state["auth_at"]):
                state["caller"] = _authenticate()
                state["auth_at"] = time.monotonic()
            pol = base_pol
            if body.get("policy") and body["policy"] != args.policy:
                pol = policy_mod.PRESETS[body["policy"]].merged(approvals=False, clarify_rounds=0, project_memory=False,
                                                                notebook=False, recall=False)
            if body.get("overrides"):
                ov = dict(body["overrides"])
                for k in ("allowed_tools", "sources"):
                    if isinstance(ov.get(k), list):
                        ov[k] = frozenset(ov[k])
                if isinstance(ov.get("blocked_sources"), list):
                    ov["blocked_sources"] = tuple(ov["blocked_sources"])
                pol = pol.merged(**ov)
            if body.get("max_steps"):
                pol = pol.merged(max_steps=int(body["max_steps"]))
            t0 = time.monotonic()
            with context.using(state["caller"]):
                db.init_db()
                gen = build_provider(args.provider, model=args.model)
                res = run_headless(str(body.get("question") or ""), gen_provider=gen, policy=pol,
                                   session_title=str(body.get("session_title") or "harness"),
                                   keep_session=not body.get("drop_session", False),
                                   enabled_skills=body.get("skills"))
            elapsed = round(time.monotonic() - t0, 1)
            row = {"usage": res.usage, "run_trace": res.run_trace or None, "trajectory": res.trajectory,
                   "error": res.error or None, "answer": res.answer}
            try:
                p = _perf.from_row(row)
            except Exception:  # noqa: BLE001 — 성능 레코드는 부가 정보
                p = {}
            return {"answer": res.answer, "report_md": res.report_md,
                    "documents": [{"name": d.get("name"), "content": d.get("content")} for d in (res.documents or [])],
                    "usage": res.usage, "cost_usd": p.get("cost_usd"), "tool_calls": p.get("tool_calls"),
                    "elapsed_s": elapsed, "error": res.error or None, "stopped": res.stopped or None,
                    "session_id": res.session_id, "policy": pol.name}

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, payload: dict) -> None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):  # noqa: N802
            if self.path.startswith("/health"):
                self._send(200, {"ok": True, "policy": args.policy, "provider": args.provider, "model": args.model})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):  # noqa: N802
            if not self.path.startswith("/solve"):
                self._send(404, {"error": "not found"})
                return
            n = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(n) or b"{}")
            except json.JSONDecodeError as exc:
                self._send(400, {"error": f"bad json: {exc}"})
                return
            if not str(body.get("question") or "").strip():
                self._send(400, {"error": "question is required"})
                return
            try:
                out = solve(body)
            except Exception as exc:  # noqa: BLE001 — 하네스에 오류를 돌려준다(문항 실패로 채점)
                print(f"solve error: {type(exc).__name__}: {exc}", file=sys.stderr)
                self._send(500, {"error": f"{type(exc).__name__}: {exc}"})
                return
            print(f"solved: {out['elapsed_s']}s ${out.get('cost_usd')} err={out.get('error')}", file=sys.stderr)
            self._send(200, out)

        def log_message(self, fmt, *a):  # noqa: D102 — 기본 액세스 로그 억제
            return

    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    srv.request_queue_size = 32
    print(f"neutropic solve service on {args.host}:{args.port} policy={args.policy} provider={args.provider}", file=sys.stderr)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
