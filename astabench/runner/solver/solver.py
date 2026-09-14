"""Neutropic solver for AstaBench — calls the Neutropic headless solve service (HTTP) per sample.

The service (`python -m app.benchmarks.serve`, run inside the Neutropic bench container) executes one
production research turn and returns the chat answer / report. The solver only formats the task prompt
and hands the final text back to the task's scorer (e.g. LitQA2 parses `{"answer": "<letter>"}`).

    inspect eval astabench/litqa2 -T with_search_tools=false -T split=dev \
        --solver solvers/neutropic/solver.py@neutropic --model google/gemini-3.8-flash --limit 5 \
        --max-connections 1 -S url=http://localhost:8765/solve

Custom-tools track: retrieval is Neutropic's own fan-out (OpenAlex · Semantic Scholar · PubMed · arXiv ·
Crossref · Europe PMC · ERIC · web), not the Asta Scientific Corpus tool. `--model` is required by Inspect
but never called here (cost is reported by the service, not by Inspect's model usage).
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.request

from inspect_ai.model import ModelOutput
from inspect_ai.solver import Generate, Solver, TaskState, solver

DEFAULT_URL = os.environ.get("NEUTROPIC_SOLVE_URL", "http://localhost:8765/solve")

# Multiple-choice (LitQA2) handling: the astabench textin prompt ends with `Answer with the letter … in JSON: {"answer": …}`.
# Gemini 3.1 Pro returns empty steps for that JSON-only instruction on some biomedical questions (observed 2026-09-13:
# 6 empty end_turn steps, 0 output tokens), so the solver replaces it with a natural-language instruction and converts the
# final letter back to the `{"answer": "<letter>"}` format the scorer parses.
_JSON_INSTRUCTION = re.compile(r"\n*Answer with the letter of the chosen answer in JSON:.*$", re.S)
MC_SUFFIX = ("\n\nSearch the literature with your tools before answering. Reply in chat (no report or document): one or two "
             "sentences of justification with the source, then a last line of the form `Final answer: <letter>`. If the "
             "sources you found do not settle the question, choose the 'Insufficient information' option.")
_FINAL = re.compile(r"final answer\s*[:：]\s*\**\(?([A-Z])\)?", re.I)
_JSON_ANS = re.compile(r'"answer"\s*:\s*"([A-Z])"')


def _letter(text: str) -> str | None:
    m = _FINAL.findall(text) or _JSON_ANS.findall(text)
    return m[-1].upper() if m else None


@solver
def neutropic(url: str = DEFAULT_URL, policy: str = "full", max_steps: int = 0, timeout: int = 3600,
              skills: str = "research-paper", overrides: str = '{"auto_report": false, "reviewer": false, "repair": false}') -> Solver:
    """`skills`: comma-separated Neutropic skills to force (default: the academic literature track — the router
    otherwise sends short questions to the quick-fact path, which drops the choices). `overrides`: JSON of RunPolicy
    fields; the default turns off report synthesis / review because a multiple-choice answer needs a chat reply,
    not a document (a full report turn costs ~5 min · $0.23 per question vs ~40 s · $0.07)."""
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        text_in = state.input_text
        multichoice = bool(_JSON_INSTRUCTION.search(text_in))
        if multichoice:
            text_in = _JSON_INSTRUCTION.sub("", text_in).rstrip() + MC_SUFFIX
        body = {"question": text_in, "policy": policy, "session_title": f"asta:{state.sample_id}"}
        if skills:
            body["skills"] = [s for s in skills.split(",") if s]
        if overrides:
            body["overrides"] = json.loads(overrides)
        if max_steps:
            body["max_steps"] = max_steps
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        t0 = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:   # noqa: S310 — local service
                out = json.loads(r.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001 — surface as an empty answer; the scorer marks it wrong
            out = {"answer": "", "error": f"{type(exc).__name__}: {exc}"}
        text = (out.get("answer") or "").strip()
        if not text and out.get("report_md"):
            text = out["report_md"]
        if multichoice:
            letter = _letter(text)
            if letter is None and "insufficient" in text.lower():
                letter = state.metadata.get("unsure_letter")
            text = f"{text}\n\n{{\"answer\": \"{letter}\"}}" if letter else text
        state.output = ModelOutput.from_content(model="neutropic", content=text or "")
        state.metadata.update({"neutropic": {k: out.get(k) for k in ("cost_usd", "elapsed_s", "tool_calls", "error",
                                                                     "stopped", "session_id", "policy")},
                               "neutropic_wall_s": round(time.monotonic() - t0, 1)})
        return state

    return solve
