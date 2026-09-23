# `augments` CLI Reference

The `augments` console script is the primary command-line interface for the
Augments ADK. It covers the full operator workflow: scaffolding a project,
validating configs, running a one-shot prompt, opening an interactive chat
session, inspecting saved sessions, publishing a JSON Schema, and serving an
agent over the A2A protocol.

---

## Installation

The CLI ships with the base package:

```bash
pip install augments-adk
```

Two commands have additional dependencies behind optional extras:

- `augments serve` — requires the `serve` extra (Starlette + uvicorn + A2A SDK):

  ```bash
  pip install 'augments-adk[serve]'
  ```

- `--trace` flag on `run` and `chat` — requires the `otel` extra:

  ```bash
  pip install 'augments-adk[otel]'
  ```

---

## Specifying a target

Every execution command (`run`, `chat`, `validate`, `serve`) accepts a
**target** in one of two forms.

**Config file path** — a `.json`, `.yaml`, or `.yml` file validated against
the published schema before use. A document with a root `agents` key is a
topology; any other document is a single-agent config.

```bash
augments run my_agent/agent.json "hello"
augments run my_topology/topology.json "hello"
```

**Dotted Python reference** — a `MODULE:VAR` string that resolves an
`Agent`, `Swarm`, or `Graph` object in user code. The current working
directory must be importable (i.e. on `sys.path` or run from the project
root).

```bash
augments run --agent my_pkg.agents:support "hello"
```

When the target is a topology, the CLI dispatches to the first available
structure in this order: **graph**, then **swarm**, then the `entry` agent.

---

## Default behaviour and explicit opt-in

The CLI is cost-conservative by design. Every feature that adds latency,
tokens, or side-effects is off unless you enable it explicitly:

- `.env` files are **never auto-discovered** — pass `--env-file <path>` to
  load one.
- Session persistence is **off by default** — pass `--session-db` to enable
  it.
- Verbose output is **off by default** — pass `--verbose` to enable it.
- Tracing is **off by default** — pass `--trace` to enable it.
- Omitting `--model` or `--max-turns` leaves the framework defaults
  untouched — the CLI never re-states a default on your behalf.

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `2` | Usage or configuration error — a guiding message is printed, no traceback |
| `1` | Unexpected runtime error |

---

## Commands

### `augments run`

Run a target once with a prompt and print the final output.

```
augments run [OPTIONS] [CONFIG] [PROMPT]
```

The prompt can be supplied as a positional argument or piped through stdin:

```bash
# Positional prompt
augments run agent.json "What is the capital of France?"

# Stdin
echo "What is the capital of France?" | augments run agent.json

# With --agent instead of a config file
augments run --agent my_pkg.agents:assistant "Summarise this report."
```

**Options**

| Flag | Description |
|------|-------------|
| `--agent MODULE:VAR` | Dotted reference to an `Agent`/`Swarm`/`Graph` object |
| `--model TEXT` | Override the model for this invocation |
| `--max-turns INTEGER` | Per-agent loop turn limit (framework default when omitted) |
| `--verbose` | Verbose output (Rich when the `[verbose]` extra is installed, ANSI otherwise) |
| `--trace` | Enable tracing with a console span exporter (requires `[otel]`) |
| `--env-file FILE` | Load `KEY=VALUE` pairs from this file (never auto-discovered) |
| `--session-db FILE` | SQLite file for session persistence; omit to keep the run in memory |
| `--session-id TEXT` | Session id to create or resume (default: `default`) |
| `--user-id TEXT` | User scope for the session (default: `default`) |
| `--output [text\|json]` | Result format on stdout (default: `text`) |
| `--stream` | Stream text deltas as they arrive (single-agent targets only) |

**Examples**

```bash
# One-shot run with JSON output
augments run agent.json "Explain caching." --output json

# Stream deltas to the terminal
augments run agent.json "Write a haiku." --stream

# Persist the conversation to a SQLite file
augments run agent.json "Hello" \
  --session-db sessions.db \
  --session-id my-session

# Resume the same session
augments run agent.json "What did I just say?" \
  --session-db sessions.db \
  --session-id my-session
```

---

### `augments chat`

Open an interactive REPL with an agent. Type `exit`, `quit`, press `Ctrl-D`,
or `Ctrl-C` to end the session. Sessions persist across invocations when
`--session-db` is given.

```
augments chat [OPTIONS] [CONFIG]
```

```bash
augments chat agent.json
augments chat --agent my_pkg.agents:assistant
```

**Options**

| Flag | Description |
|------|-------------|
| `--agent MODULE:VAR` | Dotted reference to an `Agent`/`Swarm`/`Graph` object |
| `--model TEXT` | Override the model for this invocation |
| `--max-turns INTEGER` | Per-agent loop turn limit (framework default when omitted) |
| `--verbose` | Verbose output (Rich when the `[verbose]` extra is installed, ANSI otherwise) |
| `--trace` | Enable tracing with a console span exporter (requires `[otel]`) |
| `--env-file FILE` | Load `KEY=VALUE` pairs from this file (never auto-discovered) |
| `--session-db FILE` | SQLite file for session persistence |
| `--session-id TEXT` | Session id to create or resume (default: `default`) |
| `--user-id TEXT` | User scope for the session (default: `default`) |
| `--no-stream` | Print each reply only when complete |

**Examples**

```bash
# Chat with streaming replies (default)
augments chat agent.json

# Persist the conversation; resume later with the same flags
augments chat agent.json \
  --session-db chat.db \
  --session-id project-alpha

# Disable streaming — reply printed when complete
augments chat agent.json --no-stream
```

---

### `augments validate`

Validate a config file against the published JSON Schema. No agent is
constructed and no tokens are spent.

```
augments validate [OPTIONS] CONFIG
```

```bash
augments validate agent.json
augments validate topology.yaml
```

**Options**

| Flag | Description |
|------|-------------|
| `--kind [agent\|topology]` | Override document-kind detection (a root `agents` key means topology) |
| `--resolve` | Also assemble the config, importing all dotted references |

Without `--resolve`, validation is a pure schema check — fast and offline.
With `--resolve`, the command imports every module referenced in `tools`,
`output_schema`, `guardrails`, and `system_prompt.dynamic`; it confirms the
assembled agent is structurally complete.

**Examples**

```bash
# Schema-only check (no imports)
augments validate my_agent/agent.json

# Also import tool and guardrail references
augments validate --resolve my_agent/agent.json

# Force topology parsing on a file without a root 'agents' key
augments validate --kind topology partial.json
```

---

### `augments new`

Scaffold a new project in its own directory. The generated project passes
`augments validate --resolve` with no edits.

```
augments new [OPTIONS] NAME
```

`NAME` must match `[a-z][a-z0-9_]*` — it becomes both the directory name
and the agent name.

**Options**

| Flag | Description |
|------|-------------|
| `--kind [agent\|topology]` | Scaffold a single agent or a multi-agent topology (default: `agent`) |
| `--dir DIRECTORY` | Parent directory to create the project in (default: current directory) |

**Generated files for `--kind agent`**

| File | Purpose |
|------|---------|
| `agent.json` | Agent config with a `$schema` pointer and a sample tool reference |
| `<name>_tools.py` | Python module with the sample `current_time` tool |
| `agent_config.schema.json` | Offline copy of the agent JSON Schema for editor validation |
| `.env.example` | Template for provider credentials |
| `README.md` | Quick-start instructions for the project |

**Generated files for `--kind topology`**

| File | Purpose |
|------|---------|
| `topology.json` | Topology config with a triage → expert handoff and a `$schema` pointer |
| `topology_config.schema.json` | Offline copy of the topology JSON Schema |
| `.env.example` | Template for provider credentials |
| `README.md` | Quick-start instructions for the project |

**Examples**

```bash
# Scaffold a single-agent project
augments new my_agent

# Scaffold a multi-agent topology project
augments new my_topology --kind topology

# Scaffold inside a specific parent directory
augments new my_agent --dir ~/projects
```

---

### `augments schema`

Print the JSON Schema for a config kind to stdout or write it to a file.
Useful for CI validation or editor setup.

```
augments schema [OPTIONS] [[agent|node|topology]]
```

| `KIND` | Description |
|--------|-------------|
| `agent` | Schema for a single-agent config (`AgentConfig`) |
| `node` | Schema for a sub-agent file used inside a topology (`AgentNodeConfig`) |
| `topology` | Schema for a multi-agent topology (`TopologyConfig`) |

**Options**

| Flag | Description |
|------|-------------|
| `--out FILE` | Write the schema to this file instead of stdout |

**Examples**

```bash
# Print the agent schema
augments schema agent

# Write the topology schema to a file
augments schema topology --out topology_config.schema.json

# Print the node schema (for sub-agent files referenced via config_path)
augments schema node
```

---

### `augments sessions`

Inspect and prune the session stores written by `run` and `chat`.

The `sessions` group requires `--db` and `--app-name` on every sub-command.
`--app-name` is the name the run/chat target wrote under — the agent name,
the swarm entry-agent name, or the graph `id`.

#### `augments sessions list`

List sessions in the store, oldest first.

```
augments sessions list [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--db FILE` | SQLite session store file (required) |
| `--app-name TEXT` | Application scope (the run/chat target name) (required) |
| `--user-id TEXT` | Filter by user; omit to list every user's sessions |

```bash
augments sessions list --db sessions.db --app-name my_agent
augments sessions list --db sessions.db --app-name my_agent --user-id alice
```

#### `augments sessions show`

Render a session's conversation events.

```
augments sessions show [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--db FILE` | SQLite session store file (required) |
| `--app-name TEXT` | Application scope (required) |
| `--id TEXT` | Session id to render (required) |
| `--user-id TEXT` | User scope of the session (default: `default`) |
| `--limit INTEGER` | Maximum number of events to render (all when omitted) |
| `--output [text\|json]` | Render format on stdout (default: `text`) |

```bash
augments sessions show --db sessions.db --app-name my_agent --id my-session
augments sessions show --db sessions.db --app-name my_agent --id my-session \
  --output json --limit 20
```

#### `augments sessions delete`

Delete one session and all its messages.

```
augments sessions delete [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--db FILE` | SQLite session store file (required) |
| `--app-name TEXT` | Application scope (required) |
| `--id TEXT` | Session id to delete (required) |
| `--user-id TEXT` | User scope of the session (default: `default`) |
| `--yes` | Skip the confirmation prompt |

```bash
augments sessions delete --db sessions.db --app-name my_agent --id old-session
augments sessions delete --db sessions.db --app-name my_agent --id old-session --yes
```

---

### `augments serve`

Serve a single `Agent` as an A2A endpoint.

```
augments serve [OPTIONS] [CONFIG]
```

> [!IMPORTANT]
> `augments serve` requires the `serve` extra:
>
> ```bash
> pip install 'augments-adk[serve]'
> ```

The `--card` option is **required**. The AgentCard must be a
developer-authored JSON file in protobuf JSON form (camelCase field names).
The CLI never synthesises a card. The card is published at
`GET /.well-known/agent-card.json` when the server starts.

**Options**

| Flag | Description |
|------|-------------|
| `--agent MODULE:VAR` | Dotted reference to an `Agent` object |
| `--card FILE` | Developer-authored AgentCard JSON file (required) |
| `--host TEXT` | Bind address (default: `127.0.0.1`) |
| `--port INTEGER` | Bind port (default: `8000`) |
| `--max-turns INTEGER` | Per-task agent loop turn limit (framework default when omitted) |
| `--env-file FILE` | Load `KEY=VALUE` pairs from this file (never auto-discovered) |

> [!WARNING]
> `augments serve` uses an **in-memory task store** by default. Tasks are lost
> on process restart. For production deployments, use
> `build_starlette_app` directly and supply a persistent task store — see
> [A2A guide](../a2a/a2a.md#production-warning-persistent-task-store).

**Example**

Prepare an AgentCard JSON file (camelCase, as required by the A2A protobuf
schema):

```json
{
  "name": "my-assistant",
  "description": "A helpful assistant exposed over A2A.",
  "version": "1.0.0",
  "supportedInterfaces": [
    {
      "url": "http://127.0.0.1:8000",
      "protocolBinding": "JSONRPC",
      "protocolVersion": "1.0"
    }
  ],
  "capabilities": {"streaming": true}
}
```

Then start the server:

```bash
augments serve agent.json --card card.json
augments serve --agent my_pkg.agents:assistant --card card.json --port 9000
```

---

## End-to-end workflow

The following sequence takes a new project from scaffold to interactive chat:

```bash
# 1. Scaffold a new agent project
augments new my_agent

# 2. Validate the generated config (schema-only, zero tokens)
augments validate my_agent/agent.json

# 3. Also validate that tool references import cleanly
augments validate --resolve my_agent/agent.json

# 4. Run a one-shot prompt
augments run my_agent/agent.json "What time is it?"

# 5. Open an interactive chat with session persistence
augments chat my_agent/agent.json \
  --session-db chat.db \
  --session-id my-session \
  --env-file my_agent/.env
```

---

## See also

- [Declarative configuration](../config/config.md) — the full field reference
  for agent and topology config files.
- [A2A guide](../a2a/a2a.md) — building and consuming A2A endpoints in Python.
- [Sessions guide](../session/index.md) — the session persistence subsystem.
- [Tracing guide](../tracing/index.md) — OpenTelemetry integration.
