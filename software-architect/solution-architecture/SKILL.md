---
name: solution-architecture
description: >-
  Design an end-to-end solution architecture from a framed problem and chosen
  technologies. Use to produce C4-style views (context, container, component),
  data flows and contracts, deployment topology, cross-cutting concerns
  (security, scale, reliability), and sunny/rainy scenarios. Produces the
  technical core of the architecture document.
---

# Solution architecture

## Purpose

Assemble the framed problem, evidence, and technology choices into a coherent
end-to-end design that an engineering org can build and a CTO can approve.

## Prerequisites

- `problem-framing` output (scope, NFR targets, success metrics).
- `technology-evaluation` decisions (chosen components + reasons).
- `discovery-research` Evidence Base for any capability claims.

## Instructions

1. **Structure with the C4 model** (progressive zoom):
   - **Context** — the system, its users, and external systems it talks to.
   - **Container** — deployable/runtime units (services, datastores, queues,
     gateways) and how they communicate (protocol + sync/async).
   - **Component** — internal structure of the containers that carry the most
     risk or novelty. Do not decompose everything — only what matters.
   - (Code level is out of scope for an HLD.)
2. **Make data first-class.** Define the key data entities, ownership (which
   service owns which data), and the integration contracts (inputs read, outputs
   written) per boundary. Note consistency model (strong/eventual) where it
   affects the design.
3. **Choose and name patterns** explicitly (e.g. CQRS, event-driven, saga,
   strangler-fig, sidecar, BFF) with the reason each is used. Tie back to NFRs.
4. **Design deployment topology.** Environments, regions/AZs, scaling units,
   network boundaries, and where state lives. Call out the substrate
   (Kubernetes, serverless, managed services).
5. **Address cross-cutting concerns** — each as its own short subsection:
   - Security: authN/authZ, workload identity, secrets, data protection,
     trust boundaries (align with kaif-guard / kaif-identity principles).
   - Scalability & performance: scaling strategy, bottlenecks, capacity model.
   - Reliability: failure modes, redundancy, degradation, RTO/RPO,
     backpressure, timeouts, idempotency.
   - Observability: what is measured (metrics/traces/logs), key SLOs.
6. **Write sunny- and rainy-day scenarios.** Walk one happy path and 2–3
   failure/exception paths end-to-end to prove the design holds.
7. **Request diagrams** from the `architecture-diagramming` skill for the
   context, container, one key sequence, and the deployment view.

## Output contract

A `## Solution Architecture` section:

| Subsection | Content |
|---|---|
| Solution overview | **Diagram first** (context/container), then prose |
| Architecture views | C4 context, container, key component views |
| Data & contracts | Entities, ownership, integration I/O, consistency |
| Patterns & rationale | Named pattern → why → NFR served |
| Deployment topology | Environments, regions, scaling units, substrate |
| Security & trust boundaries | authN/authZ, identity, secrets, data protection |
| Scalability & performance | Strategy, bottlenecks, capacity model |
| Reliability | Failure modes, redundancy, RTO/RPO, degradation |
| Observability | Metrics/traces/logs, SLOs |
| Scenarios | 1 sunny + 2–3 rainy, walked end-to-end |

## Quality checks

- [ ] Solution overview opens with a diagram, not prose.
- [ ] Every container has a clear responsibility and owns its data.
- [ ] Each named pattern maps to an NFR it serves.
- [ ] Trust boundaries are explicit; no static long-lived secrets in the happy
      path (prefer workload identity).
- [ ] At least one failure path is walked end-to-end.
- [ ] Deployment topology names the substrate and scaling units.
- [ ] Nothing in the design contradicts a Problem Frame constraint.

## Hand-off

Feed sizing/topology to `cost-analysis`, the component/vendor list to
`licensing-analysis`, and the build shape to `dev-team-guidelines`.
