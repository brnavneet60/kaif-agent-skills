#!/usr/bin/env python3
"""Deterministic weighted-scoring matrix for a technology bake-off.

Reads a JSON spec of weighted criteria and per-candidate scores (1-5) and prints
a ranked markdown matrix. Stdlib only — no pip, no external deps.

Usage:
  python3 score_matrix.py criteria.json
  cat criteria.json | python3 score_matrix.py -

Input JSON shape:
{
  "criteria":  [{"name": "Fit", "weight": 40}, {"name": "Maturity", "weight": 60}],
  "candidates": {"Option A": {"Fit": 5, "Maturity": 3}, "Option B": {"Fit": 4, "Maturity": 4}}
}

Scores are expected on a 1-5 scale; the weighted total is normalized to 100.
"""
from __future__ import annotations

import json
import sys

MAX_SCORE = 5


def load_spec(arg: str) -> dict:
    if arg == "-":
        return json.load(sys.stdin)
    with open(arg, encoding="utf-8") as fh:
        return json.load(fh)


def validate(spec: dict) -> tuple[list[dict], dict]:
    criteria = spec.get("criteria") or []
    candidates = spec.get("candidates") or {}
    if not criteria:
        raise SystemExit("error: 'criteria' is empty")
    if not candidates:
        raise SystemExit("error: 'candidates' is empty")

    total_weight = sum(c.get("weight", 0) for c in criteria)
    if total_weight <= 0:
        raise SystemExit("error: criteria weights must sum to > 0")
    if total_weight != 100:
        print(
            f"> note: weights sum to {total_weight}, not 100 — normalizing.\n",
            file=sys.stderr,
        )
    return criteria, candidates


def weighted_totals(criteria: list[dict], candidates: dict) -> dict:
    total_weight = sum(c["weight"] for c in criteria)
    results: dict[str, float] = {}
    for name, scores in candidates.items():
        acc = 0.0
        for crit in criteria:
            raw = scores.get(crit["name"], 0)
            # normalize score to 0..1, weight, scale to 100
            acc += (raw / MAX_SCORE) * (crit["weight"] / total_weight) * 100
        results[name] = round(acc, 1)
    return results


def render(criteria: list[dict], candidates: dict, totals: dict) -> str:
    names = list(candidates.keys())
    ranked = sorted(totals, key=lambda n: totals[n], reverse=True)
    rank_of = {n: i + 1 for i, n in enumerate(ranked)}

    header = ["Criterion (weight)"] + names
    lines = ["| " + " | ".join(header) + " |",
             "|" + "|".join(["---"] * len(header)) + "|"]

    for crit in criteria:
        row = [f"{crit['name']} ({crit['weight']})"]
        for n in names:
            row.append(str(candidates[n].get(crit["name"], "-")))
        lines.append("| " + " | ".join(row) + " |")

    total_row = ["**Weighted total /100**"] + [f"**{totals[n]}**" for n in names]
    lines.append("| " + " | ".join(total_row) + " |")
    rank_row = ["**Rank**"] + [f"#{rank_of[n]}" for n in names]
    lines.append("| " + " | ".join(rank_row) + " |")

    winner = ranked[0]
    lines.append("")
    lines.append(f"**Top score:** {winner} ({totals[winner]}/100). "
                 "Confirm the choice against business fit, risk, and "
                 "reversibility — the highest number is an input, not the verdict.")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: score_matrix.py <criteria.json|->")
    spec = load_spec(sys.argv[1])
    criteria, candidates = validate(spec)
    totals = weighted_totals(criteria, candidates)
    print(render(criteria, candidates, totals))


if __name__ == "__main__":
    main()
