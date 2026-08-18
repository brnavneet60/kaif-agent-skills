---
name: dev-team-guidelines
description: >-
  Translate the approved architecture into actionable guidelines for the
  delivery team — repo/branching, coding standards, testing strategy, CI/CD,
  security, observability, and Definition of Done. Use to produce the
  "how we build it" section so engineering can start without re-deriving intent.
---

# Development team guidelines

## Purpose

Bridge architecture to execution. The CTO/PDM approves the design; the
engineering team needs concrete, opinionated guardrails to build it consistently
and safely. This is the delivery playbook, derived from the chosen architecture
and constraints.

## Prerequisites

- `solution-architecture` (components, patterns, substrate).
- `technology-evaluation` (chosen stack).
- `licensing-analysis` (supply-chain controls to enforce in CI).

## Instructions

Produce guidelines across these areas, each concrete and tailored to the chosen
stack (avoid generic platitudes):

1. **Repository & branching.** Mono vs multi-repo (with reason), branching model
   (trunk-based recommended for CD), PR review policy, commit conventions,
   protected branches.
2. **Coding standards.** Language style guides, linters/formatters (named tools
   for the chosen stack), API design conventions (REST/gRPC/event schema),
   error-handling and logging conventions, naming.
3. **Testing strategy.** The test pyramid for this system: unit, integration,
   contract (for service boundaries), e2e, and coverage gates. Name where each
   applies to the architecture's risky components.
4. **CI/CD.** Pipeline stages (build → test → scan → sign → deploy), environment
   promotion, GitOps if applicable, rollback strategy, artifact/versioning.
5. **Security in the SDLC.** Secrets management (no secrets in Git; use a
   manager/ExternalSecret), dependency and license scanning, SAST/DAST, image
   signing (cosign), least-privilege for service accounts. Align with the
   licensing-analysis controls and OWASP.
6. **Observability by default.** Logging format, metrics/SLOs to emit, tracing
   propagation, dashboards and alerts the team must ship with each service.
7. **Definition of Done.** A checklist a story must pass: tests + coverage,
   docs, security scan clean, observability wired, reviewed, deployed to a
   non-prod env.
8. **Team topology & roles.** Suggested team shape (e.g. stream-aligned +
   platform), roles/skills needed to build and run, and ownership boundaries per
   component.

## Output contract

A `## Development Guidelines` section with a subsection per area above. Prefer
tables and checklists over prose. Every guideline should be actionable ("use X",
"gate on Y") rather than aspirational ("strive for quality").

## Quality checks

- [ ] Guidelines name specific tools for the chosen stack, not generic advice.
- [ ] Testing strategy maps test types to the architecture's risky components.
- [ ] CI/CD includes security + license scanning and image signing.
- [ ] Secrets policy: nothing sensitive in Git; a manager is specified.
- [ ] Observability requirements are shippable with each service.
- [ ] Definition of Done is a concrete checklist.
- [ ] Team topology and per-component ownership are stated.
