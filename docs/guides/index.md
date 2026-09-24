# Guides

How-to pages for the ADK's developer surface. Each guide walks through
one area end to end and links to the module-level reference docs under
`docs/<module>/` for details.

- **[Agents](agents.md)** — `Agent` configuration: name, instructions, tools, handoffs, guardrails.
- **[Tools](tools.md)** — Function tools, hosted tools, MCP tools, tool guardrails.
- **[Handoffs](handoffs.md)** — LLM-orchestrated and code-orchestrated routing.
- **[Guardrails](guardrails.md)** — User-authored input and output safety gates. Decorator-based and config `ref` patterns.
- **[Memory](memory.md)** — Episodic + semantic memory; vector stores; embedders.
- **[Skills](skills.md)** — Reusable capability bundles (instructions + tools + governance).
- **[Tracing](tracing.md)** — OpenInference / OpenTelemetry; Arize, Phoenix, Langfuse exporters.
- **[Cost](cost.md)** — CostEstimator, CostLedger, LLMRouter (CheapestFirst, LatencyFirst).
- **[Sandbox](sandbox.md)** — Sandbox-isolated tool execution; Docker / K8s / hosted-bridge clients.
- **[A2A](a2a.md)** — Agent-to-Agent protocol.
- **[MCP](mcp.md)** — Model Context Protocol client + server.
