# Working on the Augments ADK

Augments is a provider-agnostic Python **ADK** (Agent Development Kit) for
building systems of agents that act in the world, across 100+ LLMs via
litellm. Say "ADK" for this project; "SDK" is only for third parties (the
OpenAI Agents SDK, the Anthropic SDK).

These are the instructions every coding agent follows in this repository.
Keep them short and current: when you learn something the next session
would need, add it to **Memories** at the bottom.

## Get set up

- Python 3.12+ and [uv](https://docs.astral.sh/uv/). `uv sync --extra dev`
  builds `.venv` from `uv.lock`; prefix commands with `uv run`.
- `uv.lock` is the source of truth for versions, and CI installs from it with
  `UV_FROZEN=1`. Never edit it by hand: change `pyproject.toml`, run
  `uv lock`, commit both.
- Conda (`environment.yaml`) also works. `make` targets take `RUN=` to drop
  the `uv run` prefix.

## Everyday commands

| What | Command |
| --- | --- |
| Unit tests | `uv run pytest tests/unit` |
| Lint and format | `uv run ruff check src tests examples` and `uv run ruff format --check src tests examples` |
| Type check (canonical) | `uv run mypy -p augments.adk` |
| Type check (second opinion) | `uv run pyright <changed .py files>` — never the whole package inline; the nightly job does that |
| Examples | `uv run python examples/run_examples.py --auto-mode [--filter <topic>]` |
| Coverage | `make coverage` |

Work is done only when ruff, ruff format, mypy, pyright on what you touched,
and the tests are all clean. The `code-hygiene-gate` skill runs the whole
set. Fix problems at the source rather than suppressing them; a remaining
`# type: ignore[rule]` needs a one-line reason.

## Find your way around

- `src/augments/adk/` — the package. Each subpackage owns one concern:
  `agents/`, `run/` (the Runner), `llms/` (one folder per provider), `tools/`,
  `types/`, `graphs/`, `swarms/`, `flows/`, `handoffs/`, `guardrails/`,
  `memory/`, `session/`, `mcp/`, `a2a/`, `tracing/`, `sandbox/`, `cli/`, …
- `tests/unit/` mirrors the package; `tests/integration/` needs live
  services (Postgres, Redis) and runs in CI.
- `examples/` — runnable scripts grouped by topic.
- `docs/` — user documentation, rendered on augmentslabs.com.
- `.agents/` — the rules, skills and subagents described below.

## Follow the rules

The project's rules live in `.agents/rules/`, one topic per file. Claude Code
loads them for you. Every other agent reads them itself:

- **Always** read `.agents/rules/architecture.md` before your first edit. It
  holds the rules that apply everywhere: how agents, the Runner, tools and
  LLM providers relate, where types live, no implicit tokens,
  cost-conservative defaults, and what never goes into shipped files.
- **Before editing a file**, read every rule whose `paths:` front matter
  matches it:

| Rule | Applies to |
| --- | --- |
| `python-conventions.md` | all Python in `src/`, `tests/`, `examples/` |
| `testing.md` | `tests/` |
| `examples.md` | `examples/` |
| `no-version-language.md`, `no-memory-in-shipped-code.md` | `src/`, `tests/`, `docs/`, `examples/`, `README.md` |
| `llms.md`, `type-layers.md`, `items.md`, `tools-guardrails.md` | their parts of `src/augments/adk/` (see each file) |
| `agents-md.md` | this file and `CLAUDE.md` |

## Docs and changelog

- When you change a public surface, update the matching page in `docs/` and
  keep its code samples runnable.
- `docs/` explains how the ADK works now. It never records past decisions,
  roadmaps, or "follow-up" notes.
- User-visible changes get an entry under `[Unreleased]` in `CHANGELOG.md`,
  written for users (what changed and what they must do), not as an
  implementation diary.

## Git, PRs and releases

- Work on a branch, never directly on `main`. Commit at logical
  checkpoints; never use `--no-verify`.
- Conventional Commit titles (`fix(scope): …`, `feat!: …` for breaking
  changes); CI lints PR titles.
- Pushing, merging and releasing are the maintainer's decisions.
- Nobody bumps versions in a normal PR. Releases follow `RELEASING.md`:
  fold the changelog, cut `release/vX.Y.Z` with `cz bump`, and merge the
  release PR as a **merge commit** (not a squash). That merge publishes to
  PyPI and cannot be undone.

## Agent configuration

Everything shared lives in `.agents/`, and each tool reaches it in its own
way. Edit the files in `.agents/`, never through a link.

| Path | What it is | Who reads it |
| --- | --- | --- |
| `AGENTS.md` | these instructions | Codex and Kimi Code directly; Claude Code through the `@AGENTS.md` import in `CLAUDE.md` |
| `.agents/rules/*.md` | the rules above | Claude Code through the `.claude/rules` symlink; other agents as described in **Follow the rules** |
| `.agents/skills/<name>/SKILL.md` | step-by-step procedures (`add-llm-provider`, `add-hosted-tool`, `add-run-item`, `code-hygiene-gate`, `ruff-format-code`, `run-examples`) | Codex and Kimi Code natively; Claude Code through one symlink per skill in `.claude/skills/` |
| `.agents/agents/*.md` | subagent definitions (`docstring-completer`, `examples-auto-runner`) | Claude Code through the `.claude/agents` symlink; Kimi Code natively |
| `.codex/agents/*.toml`, `.kimi-code/agents/*.md` | thin wrappers that point Codex and Kimi Code at the matching `.agents/agents/` file | Codex, Kimi Code |
| `.codex/config.toml`, `.codex/rules/` | Codex settings and its shell-command policy (not instructions) | Codex |

When you add a skill, create `.agents/skills/<name>/` and link it with
`ln -s ../../.agents/skills/<name> .claude/skills/<name>`; Codex does not
follow symlinks, so the real files must stay in `.agents/`. When you add a
subagent, write it in `.agents/agents/` and add a Codex wrapper next to the
existing ones. Machine-local settings (`.claude/settings.local.json`,
`.kimi-code/local.toml`) are gitignored.

## Memories

- The project was renamed from Philharmonica to Augments (package
  `augments-adk`, repo `augments-labs/augments-adk-python`). The old name
  survives only in the released sections of `CHANGELOG.md`, and that is
  intended.
- The ruff version is pinned in three places that must move together:
  `ruff==` in `pyproject.toml`, `uv.lock`, and the ruff `rev` in
  `.pre-commit-config.yaml`. Dependabot only updates the first two.
- The `openai` extra is capped at `<3` and `anthropic` at `<1`: those majors
  break the native providers, and openai 3 also drags litellm back to a
  vulnerable release. Dependabot skips both majors; migrating to them is its
  own piece of work.
- `uv lock --offline` rewrites entries in place; a later online `uv lock`
  may reorder the file without changing any pin. Compare pins, not line
  counts, before worrying about a large lockfile diff.
- PyPI publishing uses trusted publishing from `release-publish.yml` with
  environment `pypi`, registered on the `augments-adk` project. A new PyPI
  project needs a *pending* publisher on the account's Publishing page, not
  on an existing project's page.
- CI's pip-audit covers only the core runtime dependencies; Dependabot scans
  every extra in `uv.lock`. The chromadb advisories are dismissed because
  `ChromaVectorStore` only uses Chroma in-process, never its HTTP server.
