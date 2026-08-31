"""Convert Claude/agent traces into supervised fine-tuning records.

The converter keeps tool calls explicit so a model can learn planning,
function calling, observation handling, and final-answer formatting.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def convert_trace(trace: dict[str, Any]) -> dict[str, Any]:
    messages = [{"role": "system", "content": trace.get("system", "You are a finance spreadsheet agent.")}]
    messages.append({"role": "user", "content": trace["user"]})
    for step in trace.get("steps", []):
        if step["type"] == "assistant":
            messages.append({"role": "assistant", "content": step.get("content", ""), "tool_calls": step.get("tool_calls", [])})
        elif step["type"] == "tool":
            messages.append({"role": "tool", "name": step["name"], "content": json.dumps(step["result"], ensure_ascii=False)})
    messages.append({"role": "assistant", "content": trace["final"]})
    return {"messages": messages, "metadata": trace.get("metadata", {})}


def convert_jsonl(src: str, dst: str) -> None:
    out = []
    for line in Path(src).read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(convert_trace(json.loads(line)))
    Path(dst).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    args = p.parse_args()
    convert_jsonl(args.src, args.dst)
