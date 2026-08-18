---
name: problem-framing
description: >-
  Turn a vague request into a rigorous problem statement before any solutioning.
  Use FIRST on every architecture engagement to extract domain, actors,
  jobs-to-be-done, scope boundaries, constraints, NFRs, and success metrics, and
  to record explicit assumptions for unknowns. Blocks premature design.
---

# Problem framing

## Purpose

Convert an ambiguous ask ("design an X") into a bounded, testable problem
statement that the rest of the architecture work builds on. A weak frame is the
root cause of most architecture rework. This skill runs **before**
`discovery-research`, `technology-evaluation`, and `solution-architecture`.

## When to use

- The user gives a high-level goal, an RFP, a pain point, or a one-line brief.
- Any time scope, actors, or success criteria are not yet written down.

## Instructions

1. **Extract what is stated.** From the user's input, capture verbatim: the goal,
   the domain, any named systems, volumes, deadlines, and constraints.
2. **Extrapolate what is implied, then confirm.** Infer the likely domain model
   and jobs-to-be-done, but label each inference as `Assumption` and use the
   `ask_user` tool to confirm the highest-impact unknowns (max 5 questions,
   ranked by how much they change the architecture). Do not stall on low-impact
   gaps — record a planning default instead.
3. **Draw the boundary.** State explicitly what is **in scope** and **out of
   scope**. Out-of-scope is as important as in-scope for a leadership audience.
4. **Capture NFRs as numbers, not adjectives.** "Fast" → target p95 latency.
   "Scalable" → expected RPS / data volume / growth. "Secure" → compliance
   regimes (e.g. GDPR, PCI-DSS, SOC2). If unknown, assign an assumed band and
   mark it `TBC`.
5. **Define success.** 3–6 measurable outcomes the architecture must enable
   (business KPI + a technical SLO for each where possible).
6. **Name the audience and decision.** Who reads the final doc (chief
   architect / PDM / CTO) and what decision it must unblock (fund / build-vs-buy
   / go-no-go). This steers depth and language downstream.

## Output contract

Produce a `## Problem Frame` markdown section with these subsections:

| Subsection | Content |
|---|---|
| Context & goal | 2–4 sentences, business-first |
| Actors & JTBD | Table: actor → job-to-be-done → trigger |
| In scope / Out of scope | Two bullet lists |
| Constraints | Regulatory, budget, timeline, tech mandates, org |
| NFR targets | Table: NFR → target (number) → source (measured/assumed-TBC) |
| Success metrics | Business KPI + technical SLO, measurable |
| Assumptions register | Each assumption + why + confidence (H/M/L) |
| Open decisions | Question + a recommended planning default |

## Quality checks

- [ ] Every NFR is a number or an explicitly-assumed band, never an adjective.
- [ ] In-scope and out-of-scope are both present.
- [ ] Each unknown is either an `ask_user` question or a labeled assumption — no
      silent guesses.
- [ ] Success metrics are measurable and tie to the stated audience's decision.
- [ ] No solutioning yet (no product/vendor names in the frame).

## Hand-off

Emit the Problem Frame section and the Assumptions register so downstream skills
(`discovery-research`, `technology-evaluation`, `solution-architecture`,
`cost-analysis`) can consume the constraints and NFR targets directly.
