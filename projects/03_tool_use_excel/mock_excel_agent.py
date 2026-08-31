"""Small deterministic Excel-like tool environment for agent training/eval.

No spreadsheet application is required: the environment models cells and formulas
so trajectories can be generated and scored reproducibly.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Workbook:
    cells: dict[str, float | str] = field(default_factory=dict)

    def write(self, cell: str, value: float | str) -> dict:
        self.cells[cell.upper()] = value
        return {"ok": True, "cell": cell.upper(), "value": value}

    def read(self, cell: str) -> dict:
        key = cell.upper()
        return {"ok": key in self.cells, "cell": key, "value": self.cells.get(key)}

    def sum(self, cells: list[str]) -> dict:
        values = [float(self.cells[c.upper()]) for c in cells]
        return {"ok": True, "value": sum(values), "formula": f"SUM({','.join(cells)})"}


def demo() -> None:
    wb = Workbook()
    wb.write("B2", 120.0)
    wb.write("B3", 150.0)
    print(wb.sum(["B2", "B3"]))


if __name__ == "__main__":
    demo()
