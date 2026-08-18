---
name: cost-analysis
description: >-
  Produce a capex-vs-opex and total-cost-of-ownership analysis for an
  architecture over a multi-year horizon, including cost drivers, build-vs-buy,
  scaling cost curve, and a sensitivity/assumptions table. Use when leadership
  needs the money view. Uses scripts/tco_model.py for deterministic arithmetic.
---

# Cost analysis (capex vs opex / TCO)

## Purpose

Give a CTO/PDM the financial shape of the architecture: what is up-front capital
(capex) vs recurring operating cost (opex), the total cost of ownership over 3
years, and how cost scales with load. All arithmetic is done by a script so
numbers are consistent and auditable.

## Prerequisites

- `solution-architecture` deployment topology (what runs, how much).
- `discovery-research` pricing evidence (each unit price date-stamped).

## Capex vs opex — classification

| Bucket | Examples |
|---|---|
| **Capex** (up-front / capitalized) | One-time build effort, migration, licenses bought outright, hardware, initial setup/integration |
| **Opex** (recurring) | Cloud compute/storage/egress, managed-service and SaaS subscriptions, support contracts, run-team effort, observability tooling |

Cloud pay-as-you-go is opex; a reserved-instance/committed-use prepayment is
partly capitalized — note the treatment explicitly.

## Instructions

1. **Enumerate cost drivers** from the topology: compute, storage, network
   egress, managed services, licenses, third-party APIs, and people (build +
   run).
2. **Attach unit costs** from the Evidence Base, each with an `as-of` date and
   source URL. Never invent prices.
3. **State the load assumptions** that drive variable cost (RPS, data volume,
   users, growth rate). These are the sensitivity levers.
4. **Compute with the script**, not by hand:

   ```bash
   python3 scripts/tco_model.py costs.json
   ```

   It prints: capex total, annual opex, a 3-year TCO table, and opex at low /
   expected / high load (sensitivity).
5. **Do build-vs-buy** where relevant: compare in-house build capex + run opex
   against a managed/SaaS opex-heavy option over the same horizon.
6. **Show the scaling curve** qualitatively: which driver dominates as load
   grows, and where a cheaper architecture would kick in (cost cliffs).
7. **Recommend** with the trade-off named (e.g. "buy now for speed, revisit at
   >X load where build breaks even at month N").

## Input format for the script

`costs.json`:

```json
{
  "horizon_years": 3,
  "capex": [
    {"item": "Initial build", "amount": 120000},
    {"item": "Data migration", "amount": 20000}
  ],
  "opex_monthly": [
    {"item": "Compute", "amount": 3000, "scales": true},
    {"item": "Managed DB", "amount": 1500, "scales": true},
    {"item": "Run team", "amount": 8000, "scales": false}
  ],
  "sensitivity": {"low": 0.6, "expected": 1.0, "high": 1.8}
}
```

`scales: true` items are multiplied by the sensitivity factor; fixed costs are
not.

## Output contract

A `## Cost Analysis` section:

- Capex vs opex classification table (with treatment notes).
- Cost drivers table: driver → unit cost → source (as-of) → variable/fixed.
- 3-year TCO table (from the script).
- Sensitivity: opex at low/expected/high load (from the script).
- Build-vs-buy comparison (if relevant) with break-even.
- Recommendation with the trade-off stated.

## Quality checks

- [ ] Every unit price has a source URL and an `as-of` date.
- [ ] Capex and opex are separated; committed-use treatment noted.
- [ ] Arithmetic is from the script, not free-typed.
- [ ] Load assumptions that drive variable cost are explicit.
- [ ] Sensitivity (low/expected/high) is shown, not a single point estimate.
- [ ] Recommendation names the trade-off and any break-even point.
