---
name: technology-evaluation
description: >-
  Run a rigorous head-to-head technology bake-off: candidates, weighted scoring
  criteria, evidence-backed scores, a chosen default, and named rejected
  alternates with reasons. Use when a decision needs to pick among 2+ tools,
  frameworks, platforms, or patterns. Uses scripts/score_matrix.py for
  deterministic weighted scoring.
---

# Technology evaluation (bake-off)

## Purpose

Make technology choices defensible to a CTO by showing the alternatives, the
criteria, the scores, and why the losers lost. Never present a single option as
if no others existed.

## When to use

- Choosing a database, message bus, orchestration layer, framework, cloud
  service, or architectural pattern.
- Any "should we use X or Y?" question.

## Instructions

1. **List candidates (2–5).** Include an intentional "do nothing / status quo"
   or "build vs buy" option when relevant. Rejecting good options by name builds
   trust.
2. **Define weighted criteria** tied to the Problem Frame NFRs. Typical axes:
   fit-to-requirement, maturity (CNCF status / release cadence), performance,
   operability, security posture, ecosystem/community, license/cost, team
   familiarity, lock-in. Assign weights that sum to 100.
3. **Score with evidence.** Each score (1–5) must trace to a row in the
   `discovery-research` Evidence Base. No unsourced scores.
4. **Compute deterministically.** Do the arithmetic with the script, not by
   hand:

   ```bash
   python3 scripts/score_matrix.py criteria.json
   ```

   The script reads a JSON of criteria/weights and per-candidate scores and
   prints a ranked weighted matrix as markdown. This avoids arithmetic errors in
   the LLM.
5. **Pick a default and justify it** in business terms (fit + risk + cost), not
   just the top number. Note where the winner is weak.
6. **Record rejected alternates** with the specific reason each lost (e.g.
   "sandbox maturity", "AGPL license", "operational burden").
7. **State reversibility.** Is this a one-way or two-way door? What would trigger
   revisiting the choice?

## Input format for the script

`criteria.json`:

```json
{
  "criteria": [
    {"name": "Fit to NFRs", "weight": 30},
    {"name": "Maturity", "weight": 20},
    {"name": "Operability", "weight": 20},
    {"name": "License/Cost", "weight": 15},
    {"name": "Ecosystem", "weight": 15}
  ],
  "candidates": {
    "Option A": {"Fit to NFRs": 5, "Maturity": 4, "Operability": 3, "License/Cost": 4, "Ecosystem": 5},
    "Option B": {"Fit to NFRs": 4, "Maturity": 5, "Operability": 4, "License/Cost": 3, "Ecosystem": 4}
  }
}
```

## Output contract

A `## Technology Evaluation: <decision>` section:

- Candidates list (with status-quo/build-vs-buy where relevant).
- Weighted scoring matrix (from the script) — criteria as rows, candidates as
  columns, weighted total + rank at the bottom.
- **Chosen default** + business justification + known weaknesses.
- **Rejected alternates** table: option → reason rejected.
- Reversibility note (one-way vs two-way door; revisit trigger).

## Quality checks

- [ ] At least 2 candidates; status-quo/build-vs-buy considered.
- [ ] Weights sum to 100 and map to Problem Frame NFRs.
- [ ] Every score traces to an Evidence Base row (no unsourced scores).
- [ ] Arithmetic done by the script, not free-typed.
- [ ] Each rejected option has a specific, named reason.
- [ ] Reversibility stated.
