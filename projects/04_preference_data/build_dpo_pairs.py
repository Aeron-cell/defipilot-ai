"""Build DPO preference pairs from finance-agent evaluation results."""
from __future__ import annotations

import json
from pathlib import Path


def make_pair(prompt: str, candidates: list[dict]) -> dict:
    ranked = sorted(candidates, key=lambda x: (x.get("numeric_correct", False), x.get("tool_success", 0), x.get("score", 0)), reverse=True)
    if len(ranked) < 2:
        raise ValueError("Need at least two candidates")
    return {
        "prompt": prompt,
        "chosen": ranked[0]["answer"],
        "rejected": ranked[-1]["answer"],
        "metadata": {"chosen_score": ranked[0].get("score"), "rejected_score": ranked[-1].get("score")},
    }


def build(src: str, dst: str) -> None:
    rows = json.loads(Path(src).read_text(encoding="utf-8"))
    pairs = [make_pair(row["prompt"], row["candidates"]) for row in rows]
    Path(dst).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in pairs) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    args = p.parse_args()
    build(args.src, args.dst)
