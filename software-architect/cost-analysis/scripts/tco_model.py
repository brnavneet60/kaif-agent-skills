#!/usr/bin/env python3
"""Deterministic capex/opex/TCO model for an architecture cost analysis.

Reads a JSON of capex, monthly opex, and sensitivity factors and prints a
markdown cost summary: capex total, annual opex, an N-year TCO table, and opex
under low/expected/high load. Stdlib only — no pip, no external deps.

Usage:
  python3 tco_model.py costs.json
  cat costs.json | python3 tco_model.py -

Currency is unit-agnostic; format the numbers with your currency in prose.
"""
from __future__ import annotations

import json
import sys


def load_spec(arg: str) -> dict:
    if arg == "-":
        return json.load(sys.stdin)
    with open(arg, encoding="utf-8") as fh:
        return json.load(fh)


def fmt(n: float) -> str:
    return f"{n:,.0f}"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: tco_model.py <costs.json|->")
    spec = load_spec(sys.argv[1])

    years = int(spec.get("horizon_years", 3))
    capex_items = spec.get("capex", []) or []
    opex_items = spec.get("opex_monthly", []) or []
    sens = spec.get("sensitivity", {"low": 0.6, "expected": 1.0, "high": 1.8})

    capex_total = sum(i.get("amount", 0) for i in capex_items)

    fixed_monthly = sum(i["amount"] for i in opex_items if not i.get("scales"))
    scaling_monthly = sum(i["amount"] for i in opex_items if i.get("scales"))

    def monthly_at(factor: float) -> float:
        return fixed_monthly + scaling_monthly * factor

    expected_monthly = monthly_at(sens.get("expected", 1.0))
    annual_opex = expected_monthly * 12

    out: list[str] = []

    out.append("### Capex\n")
    out.append("| Item | Amount |")
    out.append("|---|---|")
    for i in capex_items:
        out.append(f"| {i.get('item','?')} | {fmt(i.get('amount',0))} |")
    out.append(f"| **Total capex** | **{fmt(capex_total)}** |\n")

    out.append("### Monthly opex (expected load)\n")
    out.append("| Item | Amount/mo | Variable |")
    out.append("|---|---|---|")
    for i in opex_items:
        out.append(
            f"| {i.get('item','?')} | {fmt(i.get('amount',0))} | "
            f"{'yes' if i.get('scales') else 'no'} |"
        )
    out.append(f"| **Total/mo** | **{fmt(expected_monthly)}** | |")
    out.append(f"| **Total/yr** | **{fmt(annual_opex)}** | |\n")

    out.append(f"### {years}-year TCO (expected load)\n")
    out.append("| Year | Capex | Opex | Cumulative |")
    out.append("|---|---|---|---|")
    cumulative = 0.0
    for y in range(1, years + 1):
        capex_y = capex_total if y == 1 else 0.0
        opex_y = annual_opex
        cumulative += capex_y + opex_y
        out.append(f"| {y} | {fmt(capex_y)} | {fmt(opex_y)} | {fmt(cumulative)} |")
    out.append(f"| **Total** | | | **{fmt(cumulative)}** |\n")

    out.append("### Opex sensitivity (annual)\n")
    out.append("| Scenario | Factor | Annual opex |")
    out.append("|---|---|---|")
    for label in ("low", "expected", "high"):
        if label in sens:
            factor = sens[label]
            out.append(f"| {label} | {factor} | {fmt(monthly_at(factor) * 12)} |")
    out.append("")
    out.append("> Scaling opex items are multiplied by the sensitivity factor; "
               "fixed items (e.g. run team) are held constant.")

    print("\n".join(out))


if __name__ == "__main__":
    main()
