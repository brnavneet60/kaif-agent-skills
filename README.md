# kaif-agent-skills

Reusable [kagent](https://kagent.dev/docs/kagent/examples/skills) skills for KAIF
agents. Each skill is a directory containing a `SKILL.md` (YAML frontmatter
`name` + `description`, then instructions) plus optional stdlib-only Python
scripts. Agents load skills via `spec.skills.gitRefs` (Git) or `spec.skills.refs`
(OCI).

## Collections

| Collection | For agent | Skills |
|---|---|---|
| [`software-architect/`](software-architect/) | `software-architect` | problem-framing, discovery-research, technology-evaluation, solution-architecture, architecture-diagramming, cost-analysis, licensing-analysis, dev-team-guidelines, architecture-document |

See each collection's `README.md` for the skill catalogue, required MCP tools,
and wiring notes.

## Layout

```
<collection>/
  <skill-name>/
    SKILL.md            # frontmatter (name, description) + instructions
    scripts/            # optional, stdlib-only Python 3 (no pip)
```

## Using a collection from an agent (Git skills)

```yaml
spec:
  skills:
    gitRefs:
      - repo: https://github.com/brnavneet60/kaif-agent-skills.git
        # subPath: software-architect   # load a single collection
        # branch: main
    # gitAuthSecretRef: { name: <secret> }   # only if the repo is private
```

kagent pulls the repo at startup, extracts skills to `/skills`, and registers a
tool per skill plus `read_file` / `write_file` / `edit_file` / `bash`.

## Conventions

- Scripts are **stdlib-only** so they run under the kagent python runtime with no
  `pip install`.
- Keep `SKILL.md` descriptions specific — that text is the always-on hint the LLM
  uses to decide when to load the skill.
- No secrets in skill files.
