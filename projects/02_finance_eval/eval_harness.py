"""Evaluation harness for finance/Excel-agent outputs.

Metrics focus on exact numeric correctness, tolerance-aware values,
required citations/formulas, tool-call success, and stability across repeats.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable


@dataclass
class EvalCase:
    case_id: str
    expected_value: float
    tolerance: float = 1e-6
    required_tokens: tuple[str, ...] = ()


@dataclass
class EvalResult:
    case_id: str
    numeric_ok: bool
    required_tokens_ok: bool
    tool_success_rate: float
    score: float


def score_case(case: EvalCase, predicted_value: float, answer: str, tool_runs: Iterable[bool]) -> EvalResult:
    numeric_ok = abs(predicted_value - case.expected_value) <= case.tolerance
    required_tokens_ok = all(token in answer for token in case.required_tokens)
    runs = list(tool_runs)
    tool_success_rate = mean(runs) if runs else 1.0
    score = 0.65 * float(numeric_ok) + 0.15 * float(required_tokens_ok) + 0.20 * tool_success_rate
    return EvalResult(case.case_id, numeric_ok, required_tokens_ok, tool_success_rate, score)


def aggregate(results: list[EvalResult]) -> dict[str, float]:
    if not results:
        return {"accuracy": 0.0, "stability": 0.0, "overall": 0.0}
    return {
        "accuracy": mean(float(r.numeric_ok) for r in results),
        "stability": mean(r.tool_success_rate for r in results),
        "overall": mean(r.score for r in results),
    }


if __name__ == "__main__":
    sample = EvalCase("dcf-wacc", 0.083, tolerance=1e-4, required_tokens=("WACC",))
    print(score_case(sample, 0.08301, "WACC = 8.301%", [True, True, True]))
