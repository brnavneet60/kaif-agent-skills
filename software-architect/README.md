# software-architect skills

kagent skill collection that upgrades the `software-architect` agent from an
LLM-only responder into a standalone architect that frames a problem, researches
evidence, evaluates technologies, designs an end-to-end architecture with
diagrams, does cost and licensing analysis, writes delivery guidelines, and
publishes an executive-grade document to Gitea.

**Status: DRAFT for review. Not yet deployed to the agent.** Nothing under
`clusters/` has been changed.

## Skills

| Skill | Purpose | Extra scripts |
|---|---|---|
| `problem-framing` | Turn a vague ask into scope, actors, NFR targets, success metrics | — |
| `discovery-research` | Evidence-backed research via `web_search` + `firecrawl` | — |
| `technology-evaluation` | Weighted bake-off: candidates → scores → default + rejected | `scripts/score_matrix.py` |
| `solution-architecture` | End-to-end C4 design, data contracts, cross-cutting concerns | — |
| `architecture-diagramming` | Mermaid C4 / sequence / deployment diagrams | — |
| `cost-analysis` | Capex vs opex, 3-yr TCO, sensitivity, build-vs-buy | `scripts/tco_model.py` |
| `licensing-analysis` | OSS/commercial license risk, copyleft flags, SBOM | — |
| `dev-team-guidelines` | Repo, testing, CI/CD, security, observability, DoD | — |
| `architecture-document` | Assemble all sections + publish to Gitea | — |

Intended run order: framing → research → evaluation → architecture (+ diagrams)
→ cost / licensing / guidelines → document. The agent loads each skill on demand
by reading its `SKILL.md`; it does not have to run them in a fixed sequence.

Scripts are **stdlib-only Python 3** (no pip) so they run with the `bash` tool
inside the kagent python runtime. Both have been smoke-tested locally.

## How kagent loads these

At startup kagent pulls the skills, extracts them to `/skills`, and registers a
tool per skill plus `read_file` / `write_file` / `edit_file` / `bash`. The agent
reads a `SKILL.md` to learn when and how to use each capability.
Source: [kagent — add skills to agents](https://kagent.dev/docs/kagent/examples/skills).

## Tools the agent must have (in addition to skills)

Skills give *instructions*; these MCP tools do the *actions*. The agent needs:

| Tool | From RemoteMCPServer | Used by |
|---|---|---|
| `web_search` | `serper` | discovery-research |
| `firecrawl_search`, `firecrawl_scrape`, `firecrawl_map` | `firecrawl` | discovery-research |
| `store_report` | `gitea-reports` | architecture-document |

`serper` and `firecrawl` are already used by `market-researcher` on
rancher-desktop. `gitea-reports` currently exists as a doks-dev overlay
(`clusters/doks-dev/overlays/remotemcpserver-gitea-reports.yaml`) — for
rancher-desktop it must be applied and pointed at a repo (see open decisions).

## Deployment options (decide at review)

Two supported packaging modes — see the kagent skills doc:

1. **OCI skills** (`spec.skills.refs`) — build a `FROM scratch` image per skill
   (or one image for the whole folder), push to a registry, reference by image.
   Fits the KAIF signed-image / supply-chain posture. Needs a registry reachable
   from the cluster.
2. **Git skills** (`spec.skills.gitRefs`, optional `gitAuthSecretRef`) — point
   the agent at a Git repo/subpath. Simplest for GitOps; the in-cluster Gitea can
   host a `kaif-agent-skills` repo. No image build step.

Recommendation: **Git skills** for the first iteration (fastest loop, no
registry), then move to **OCI** once the set stabilizes, for signing and
immutable versioning.

## Draft agent wiring (for review — not applied)

Illustrative only; final form depends on the deployment option chosen above.

```yaml
apiVersion: kagent.dev/v1alpha2
kind: Agent
metadata:
  name: software-architect
  namespace: kagent
spec:
  type: Declarative
  description: >
    Standalone software architect: frames problems, researches, evaluates tech,
    designs end-to-end architectures with diagrams, does cost/licensing analysis,
    writes dev guidelines, and publishes to Gitea.
  skills:
    # Option 2 (Git) shown; Option 1 uses refs: [ registry/...:tag ]
    gitRefs:
      - repo: http://gitea.<ns>.svc.cluster.local/kaif/kaif-agent-skills.git
        # subPath: software-architect   # if the repo holds multiple collections
        # branch: main
    # gitAuthSecretRef: { name: gitea-token }   # if the repo is private
  declarative:
    modelConfig: llm-software-architect
    runtime: python
    stream: false
    systemMessage: |
      You are a senior software architect for a chief-architect / PDM / CTO
      audience. Use your skills in order: frame the problem, research with
      evidence, evaluate technologies as a bake-off, design the end-to-end
      architecture with diagrams, then cost, licensing, and delivery guidelines,
      and finally assemble and publish the document to Gitea.
      Separate fact (cited) from recommendation (reasoned). Label unknowns as
      planning assumptions. Do not invent versions, pricing, or licenses.
    tools:
      - type: McpServer
        mcpServer:
          name: serper
          kind: RemoteMCPServer
          apiGroup: kagent.dev
          toolNames: [web_search]
      - type: McpServer
        mcpServer:
          name: firecrawl
          kind: RemoteMCPServer
          apiGroup: kagent.dev
          toolNames: [firecrawl_search, firecrawl_scrape, firecrawl_map]
      - type: McpServer
        mcpServer:
          name: gitea-reports
          kind: RemoteMCPServer
          apiGroup: kagent.dev
          toolNames: [store_report]
    deployment:
      replicas: 1
      resources:
        requests: { cpu: 50m, memory: 256Mi }
        limits:   { cpu: "1", memory: 1Gi }
```

## Open decisions (need your call before deploy)

1. **Packaging:** Git skills (recommended first) vs OCI images.
2. **Skills repo:** create `kaif-agent-skills` in the in-cluster Gitea? Public or
   private (private ⇒ `gitAuthSecretRef`)?
3. **Output repo:** dedicated `architecture-docs` Gitea repo vs reuse
   `research-reports`. `architecture-document` currently parameterizes
   `repo_name`.
4. **`gitea-reports` on rancher-desktop:** apply the RemoteMCPServer + token
   secret (only doks-dev has it today).
5. **Observability:** keep `X-Kaif-Flow=architecture`; add per-skill labels
   later via the scenario/skill header mechanism (separate thread).
6. **Cost of tools:** research + crawl add token/LLM cost and external API usage
   (Serper/Firecrawl keys). Confirm those secrets exist on rancher-desktop.
