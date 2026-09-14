"""Task wrappers for the custom-tools track (Neutropic's own retrieval; no Asta Scientific Corpus tool).

The astabench `litqa2` wrapper task swallows `-T with_search_tools=...` (it forwards **kwargs and Inspect drops unknown
params), so these wrappers pin the arguments explicitly.

    inspect eval solvers/neutropic/tasks.py@litqa2_notools -T split=all --solver solvers/neutropic/solver.py@neutropic ...
"""
from __future__ import annotations

from typing import Literal

from inspect_ai import task

from astabench.evals.labbench.litqa2.task import litqa2


@task
def litqa2_notools(split: Literal["dev", "test", "all"] = "all", seed: int = 0):
    return litqa2(seed=seed, with_search_tools=False, with_native_search_tools=False, split=split)
