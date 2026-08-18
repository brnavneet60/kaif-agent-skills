---
name: discovery-research
description: >-
  Gather current, evidence-backed facts for architecture decisions using
  web_search (Serper) and firecrawl (search/scrape/map). Use when you need
  versions, GA status, pricing, benchmarks, CVEs, CNCF maturity, or vendor
  capabilities. Enforces primary-source citation and separates fact from
  opinion. Feeds technology-evaluation and cost-analysis.
---

# Discovery & research

## Purpose

Produce a cited evidence base so architecture claims are auditable, not
speculation. Model capabilities, pricing, and project maturity change fast; this
skill makes the agent verify before asserting.

## Tools this skill drives

- `web_search` (Serper) — current facts, news, release dates.
- `firecrawl_search` — discovery across sources when the exact page is unknown.
- `firecrawl_scrape` — pull a known URL (docs, release notes, pricing page).
- `firecrawl_map` — enumerate a site (e.g. a docs section) before scraping.

## Instructions

1. **Search before asserting.** For every non-obvious claim (version, GA status,
   pricing, benchmark, CVE, CNCF sandbox/incubating/graduated), run a search.
   Never state a volatile fact from memory.
2. **Prefer primary sources**, in this order: official docs / release notes /
   source repo → CNCF / standards bodies (OWASP, NIST, OTel, SPIFFE) → vendor
   engineering blogs with reproducible benchmarks → independent technical
   reviews (corroborate with a primary source). Avoid SEO farms and undated
   Stack Overflow.
3. **Scrape for depth.** Use `firecrawl_map` to find the right page on a large
   docs site, then `firecrawl_scrape` to read it. Use `firecrawl_search` when
   you do not yet know the source.
4. **Date-stamp volatile facts.** Write "as of <month/year>" next to versions,
   pricing, and maturity claims.
5. **Separate fact from opinion.**
   - `Fact:` "Argo CD supports ApplicationSet since v2.3" + URL.
   - `Opinion:` "For this workload Argo CD fits better because…" + reasoning.
6. **Record every source.** Maintain an evidence table as you go; do not dump
   URLs into the narrative.
7. **Say what you could not verify.** If a fact is unavailable, state what was
   searched and propose a verification step (PoC, check release notes) rather
   than guessing.

## Output contract

A `## Evidence Base` section containing:

| Column | Meaning |
|---|---|
| Claim | The fact being supported |
| Type | Primary / Secondary / Assumption |
| Source | Resolvable `https://` URL (Primary/Secondary) |
| As-of | Month/Year for volatile facts |
| Notes | Caveats, contradicting sources, confidence |

Plus a short `Key findings` list summarizing what the evidence implies for the
architecture (this is opinion — label it).

## Quality checks

- [ ] Every Primary/Secondary row has an external `https://` URL.
- [ ] Volatile facts (versions, pricing, maturity, CVEs) are date-stamped.
- [ ] Fact and opinion are visually separated.
- [ ] Unknowns are stated with a proposed verification step, not invented.
- [ ] No vendor marketing claim is used as a benchmark without a primary source.

## Hand-off

Pass the Evidence Base to `technology-evaluation` (scoring inputs) and
`cost-analysis` (pricing inputs). Every downstream citation must trace back to a
row here.
