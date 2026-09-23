# Changelog

<!--include-from-here-->

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **BREAKING:** the project is renamed to Augments, and the package is now
  published as `augments-adk` (the 0.2.3 entry below names the previous
  package). Everything that carried the previous name now carries `augments`,
  with no aliases left behind. To upgrade:
  - **Install and import.** `pip install augments-adk`, then `import augments.adk`.
    Extras keep their names (`augments-adk[otel]`, …).
  - **CLI.** The command is `augments` (`augments run`, `augments serve`, …).
    Regenerate Dockerfiles, Helm charts and AWS manifests produced by
    `augments deploy`, or edit their `CMD`, requirements line and image name
    (`augments-agent:latest`).
  - **Public classes.** The exception base is `AugmentsError`, and the Temporal
    and Restate integrations are `AugmentsWorkflow`,
    `AugmentsTemporalPlugin`, `AugmentsRestateService` and
    `build_augments_data_converter`. Update `except` clauses and imports.
  - **Temporal.** The workflow type is registered as `AugmentsWorkflow`.
    Drain or finish in-flight workflows started under the previous type name
    before deploying workers on this release; they will not resume on it.
  - **Telemetry.** The default OTel service, tracer and meter name is
    `augments-adk`; metric names and span attribute keys use the `augments.`
    prefix, and `gen_ai.system` / `llm.system` report `augments`. Update
    dashboards, alerts and queries that filter on the previous names.
  - **Logging.** Loggers live under `augments.adk`, and the default log file
    is `augments_adk.*.log`. Update logging configs that name the previous
    logger.
  - **Declarative config.** `module:attr` references and `$schema` paths that
    point into the package now start with `augments.adk` / `src/augments/`.
  - **Sandboxes.** Docker volumes are named `augments-{slug}-{digest}`, the
    local snapshot directory is `augments-adk/sandbox/snapshots` under the
    platform state directory, and Kubernetes resources carry
    `app.kubernetes.io/managed-by: augments-adk` plus `augments.adk.io/*` and
    `augments.sandbox/*` labels and annotations. Volumes, snapshots and pods
    created by earlier releases are no longer found or cleaned up; remove
    them by their previous names once no run needs them.
  - **Web loader.** The RAG website loader sends
    `User-Agent: augments-adk-document-search/1.0`.
  - **Contributors.** The repository is `augments-labs/augments-adk-python`
    (the previous URL redirects; point an existing clone at it with
    `git remote set-url origin https://github.com/augments-labs/augments-adk-python.git`),
    the conda environment is
    `augments-adk-python`, and the test and example variables are
    `AUGMENTS_TEST_PG_DSN`, `AUGMENTS_TEST_REDIS_URL` and
    `AUGMENTS_EXAMPLES_INTERACTIVE_MODE`.

## [0.2.3] - 2026-09-23

### Changed

- The project is being renamed, and this is the last release published as
  `philharmonica-adk`. Later releases ship under the new name, which the
  repository README announces.

- The `openai` extra now requires `openai<3` and the `anthropic` extra
  `anthropic<1`. Both new majors break the native provider paths: openai 3
  moves its transport to `httpx2`, and anthropic 1 no longer accepts
  `temperature`, `top_p` or `top_k` on `messages.create()`. Left uncapped, an
  install could also resolve litellm back to a release with known
  vulnerabilities to make room for openai 3.

### Fixed

- `philharmonica run` read piped prompts through `click.get_text_stream`, which
  click 8.5 deprecates; it now reads `sys.stdin` directly, with no change in
  behavior.

- `httpx` is now a declared core dependency. The package imports it on its
  core path (`LLMConfig.timeout` is typed with `httpx.Timeout`), but a base
  install only received it transitively through litellm, so a litellm release
  that dropped it would have broken `import philharmonica.adk`.

## [0.2.2] - 2026-08-08

### Fixed

- Two values that reach the type checker as a bare `object` are now narrowed
  where they are proven rather than left to inference. Decoding a pgvector row
  probed for `to_list` with `hasattr`, which cannot attach an attribute to
  `object`; the method is looked up with `getattr` instead. The duck-typing it
  guards is deliberate and stays — pgvector 0.4 and 0.5 both expose `Vector`,
  but only the later one answers `to_list()`, so an `isinstance` check would
  send 0.4 down the wrong branch. Coercing an `apply_patch` operation mapping
  validated the operation kind against a hand-written set of literals, which
  does not narrow to the declared union; the accepted values are now derived
  from that type alias, so the check and the type it proves cannot drift apart.
  Neither change alters what these functions accept or return. Both paths also
  gained the offline tests they were missing: the row decoder had none at all,
  its only suite being gated on live Postgres, and operation coercion exercised
  one of the three declared kinds.

- The nightly `pyright` job had never produced a result. Its cost was attributed
  to parsing the whole litellm dependency graph; measuring showed the opposite —
  the package checks in seconds, and the subpackage that imports litellm is
  among the fastest. Two functions in the run loop are each independently
  non-convergent for pyright, and with no timeout on the job, a run could hold a
  runner for six hours and leave no downloadable log behind. That one file is
  excluded from the check until those functions are split, and both nightly jobs
  now carry a timeout, so the gate terminates and reports.

- The live-LLM end-to-end tests raised `Missing credentials` instead of skipping
  when no API key was available. GitHub Actions substitutes an empty string for
  an absent secret, so the environment variable existed and a presence check
  passed. An empty value now counts as absent, and the tests skip as intended.

## [0.2.1] - 2026-08-08

### Added

- `uv.lock` is verified against `pyproject.toml` on every pull request. The lock
  records the workspace root's own version, and nothing checked it: the rest of
  CI runs under `UV_FROZEN`, which installs the lock as-is rather than asserting
  it is current. A release bump rewrote only the two locations commitizen is
  told about, so the lock quietly fell a version behind — while a plain local
  `uv run` re-locked it, handing contributors a modified file they had not
  touched. The release workflow now re-locks straight after the bump, and
  `uv lock --check` fails the pull request if the two ever disagree.

### Fixed

- `import philharmonica.adk.mcp` raised `ModuleNotFoundError: No module named
  'httpx2'` instead of degrading to `None` bindings when the `mcp` extra was
  not installed. That extra installs two distributions — the `mcp` client and
  `httpx2` — but the guard swallowed only `ImportError(name="mcp")`, and
  `httpx2` is the name actually seen first, since the streamable HTTP
  transport imports it at module level. Both names are now recognised as "the
  extra is absent". The equivalent guard in `philharmonica.adk.tools.toolsets`
  gained the same set; it was unreachable in practice only because
  `MCPToolset` defers its client imports.

## [0.2.0] - 2026-08-08

### Security

- The data-URL pattern behind the multimodal `File` / `Image` types matched in
  exponential time. A `File` argument of the form `data:a/b` followed by a run
  of semicolons and no comma forced the engine through every partition of that
  run: 0.53s at 24 semicolons, and at 40 it does not finish. Since these types
  parse LLM-supplied tool arguments, a single argument could hang the process.
  The pattern is now unambiguous and matches in linear time, accepting exactly
  the same URLs.
- RAG loader routing selected the YouTube and GitHub loaders by testing whether
  the URL's `netloc` *contained* their domain. A netloc carries userinfo, so
  `https://youtube.com@evil.com/watch` routed to the YouTube loader while the
  origin fetched was `evil.com`; `evil-youtube.com.attacker.net` matched on
  suffix alone. Routing now compares the parsed hostname against a domain set
  by equality or subdomain.

### Removed

- **`MCPServerWebsocket` and `MCPServerWebsocketParams`.** The MCP client
  library dropped its WebSocket client, so there is no transport left to wrap.
  Use `MCPServerStreamableHttp`, which carries server-pushed messages over the
  same connection.
- **`UnsupportedTransportError`.** The WebSocket transport was its only
  raiser; nothing in the framework raises it now.

### Changed

- **The `mcp` extra now requires `mcp>=2.0.0`.** The transports are built
  against `streamable_http_client` and the `httpx2` client types, neither of
  which the 1.x line provides.
- **`MCPServerStreamableHttpParams.httpx_client` and `.httpx_client_factory`
  now take `httpx2` objects** (`httpx2.AsyncClient`, `httpx2.Timeout`,
  `httpx2.Auth`) rather than `httpx` ones. `httpx2` is a separate
  distribution that installs alongside `httpx`; the two sets of types are not
  interchangeable. A client you supply yourself stays yours to close; one built
  by the factory is closed with the transport.
- **`MCPServer.read_resource(uri)` forwards the URI string unchanged** instead
  of parsing it into a `pydantic.AnyUrl` first. The protocol types this field
  as an opaque string and leaves scheme interpretation to the server, so URIs
  a strict URL parser rejects now reach the server.

## [0.1.1] - 2026-08-08

### Fixed

- `examples/skills/skills_agent_with_skills.py`: the tool input guardrail read
  `data.agent_output`, which `ToolInputGuardrailData` does not define, so the
  example raised `AttributeError` on its first tool call. It now reads
  `data.context.tool_arguments`.
- `examples/tools/deferred_tools_hitl.py`: the conditional-approval callback
  dereferenced `ctx.context` in a scenario that runs without one, raising
  `AttributeError` on `None`. It now falls back to the non-production branch.
- `examples/config/run_config_agent.py` and
  `examples/tools/tool_advanced_features.py`: reading `.name` off a tool
  collection that can also hold hosted tools and toolsets, neither of which
  defines it.
- `examples/skills/skills_customer_support.py`: the demo account store was
  typed loosely enough that arithmetic on a balance was unsound.
- Assorted typing repairs across the examples suite (`run_examples.py`,
  `toolsets_basic.py`, `llm_orchestrated.py`, `human_in_the_loop.py`,
  `middleware_basic.py`, `agent_guardrails.py`, `message_filters.py`,
  `run_topology.py`).

### Added

- The examples suite is type-checked on every pull request. It was previously
  excluded from the type checker, so a broken attribute access in a shipped
  example could not fail any gate.

### Changed

- The README header logo renders at 256px wide.

## [0.1.0] - 2026-08-07

### Added

- Initial public release of Philharmonica ADK as `philharmonica-adk`: the
  `philharmonica.adk` Python namespace, the `philharmonica` command-line interface, and
  the full agent development toolkit.
