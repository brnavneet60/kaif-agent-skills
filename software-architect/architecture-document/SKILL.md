---
name: architecture-document
description: >-
  Assemble the outputs of the other architect skills into one executive-grade,
  end-to-end architecture document for chief architects, PDMs, and CTOs, then
  persist it to Gitea via the gitea-reports store_report tool. Use LAST, once the
  problem, research, evaluation, design, cost, licensing, and guidelines sections
  exist.
---

# Architecture document (assemble + publish)

## Purpose

Combine the section outputs from the other skills into a single, coherent,
leadership-ready markdown document and push it to Gitea. This is the deliverable
the user receives a link to.

## Audience & tone

Readers are **chief architects, PDMs, and CTOs**. Therefore:

- Lead with business outcomes; explain technical choices through their impact.
- Every major decision states rationale, trade-off, and why chosen.
- Keep the executive narrative clean; put source URLs in the Evidence Register
  and deep engineering detail in an appendix.
- Separate **fact** (cited) from **recommendation** (reasoned).
- Label unknowns `Assumption — planning default`; never invent confirmed policy.

## Prerequisites (section inputs)

Collect the section outputs produced earlier in the engagement:

- Problem Frame (`problem-framing`)
- Evidence Base (`discovery-research`)
- Technology Evaluation (`technology-evaluation`)
- Solution Architecture + diagrams (`solution-architecture` +
  `architecture-diagramming`)
- Cost Analysis (`cost-analysis`)
- Licensing & Supply-Chain (`licensing-analysis`)
- Development Guidelines (`dev-team-guidelines`)

If any are missing, either run that skill first or include the section with an
explicit `TBC` note — do not silently omit it.

## Document structure

```
# <Solution name> — Architecture

1. Executive summary          (problem, recommended approach, value, cost, risks)
2. Problem & context          (from Problem Frame)
3. Success metrics & NFRs
4. Solution overview          (DIAGRAM FIRST, then prose)
5. Architecture views         (C4 context/container/component)
6. Key decisions & trade-offs (Decision Register + Technology Evaluation)
7. Data & integration contracts
8. Security & trust boundaries
9. Reliability & scalability
10. Cost analysis             (capex/opex, 3-yr TCO, sensitivity)
11. Licensing & supply chain
12. Delivery plan & dev guidelines
13. Risks (owner, trigger, mitigation)
14. Open decisions + recommended defaults
15. References & Evidence Register
Appendix A — engineering detail
```

## Assembly instructions

1. **Write the executive summary last**, after all sections exist, so it
   reflects the real recommendation, cost band, and top risks.
2. **Solution overview opens with a diagram** (context + container from
   `architecture-diagramming`), then prose.
3. **Build a Decision Register**: each major choice → business reasoning →
   trade-off → why chosen. Pull rejected options from the Technology Evaluation.
4. **Consolidate the Evidence Register** from the Evidence Base: every
   Primary/Secondary claim has a resolvable `https://` URL; assumptions labeled.
5. **Ensure every open decision has a recommended default** with reasoning.
6. **Consistency pass:** component names match across prose and all diagrams;
   numbers match the cost script output; no contradictions with the Problem
   Frame.

## Publish to Gitea

Persist with the `store_report` tool from the `gitea-reports` MCP server. Pass a
**non-empty** `report_markdown`:

```
store_report(
  report_markdown = <full assembled markdown>,
  report_path     = "architecture/<solution-slug>-<YYYYMMDD>.md",
  commit_message  = "architecture: <solution-slug> <YYYYMMDD>",
  branch          = "",
  repo_name       = "<architecture repo, e.g. architecture-docs>"
)
```

- If `store_report` returns an error, retry **once** with the markdown filled.
- Copy the returned `sha` and `html_url` verbatim into your reply — do not invent
  them.
- Report `PUBLISH_FAILED` if persistence fails after the retry, and still return
  the full markdown to the user so nothing is lost.

Immediately after persist (or persist failure), call `store_run_record` so
kaif-value can score the job:

```
store_run_record(
  run_id = "<kagent session id or YYYYMMDD-HHMM-short>",
  repo_name = "architecture-docs",
  card_json = {
    "run_id": "<same>",
    "flow": "architecture",
    "scenario": "<catalog enum or unknown>",
    "agent": "software-architect",
    "status": "PUBLISHED | PUBLISH_FAILED | BLOCKED_ON_USER | INCOMPLETE",
    "started_at": "<ISO-8601>",
    "ended_at": "<ISO-8601>",
    "hitl_wait_s": 0,
    "artifact": {"sha": "<from store_report or null>", "url": "<html_url or null>", "path": "<report_path or null>"}
  }
)
```

Do not put tokens, USD, or quality_score on the card — the kaif-value enricher
fills those from Prometheus and the Gitea blob.

## Reply contract

Keep the chat reply short; the document lives in Gitea:

```
STATUS: PUBLISHED | PUBLISH_FAILED | BLOCKED_ON_USER | INCOMPLETE
doc_path: architecture/<slug>-<date>.md
doc_sha:  <sha or none>
doc_url:  <html_url or none>
run_id:   <run_id passed to store_run_record>
summary:  <2-3 lines: recommendation + cost band + top risk>
```

## Quality checks (Definition of Done)

- [ ] Executive summary present and written against the final recommendation.
- [ ] Solution overview opens with a diagram.
- [ ] Decision Register present; rejected options named with reasons.
- [ ] Cost section numbers come from the cost script (consistent throughout).
- [ ] Licensing flags (AGPL/SSPL/BSL) surfaced if present.
- [ ] Every open decision has a recommended default.
- [ ] Evidence Register: every Primary/Secondary row has an external https URL.
- [ ] Component names consistent across prose and all diagrams.
- [ ] Document persisted to Gitea (sha + url) or PUBLISH_FAILED reported.
