# MCP

Model Context Protocol integration: server transports, lifecycle
management, and tool filtering.

The `mcp` package is an optional extra. When it is not installed, every
name below is bound to `None` so callers can detect availability without
`ImportError` handling.

## Servers and transports

- `augments.adk.mcp.MCPServerWithClientSession`
- `augments.adk.mcp.MCPServerStdio`
- `augments.adk.mcp.MCPServerStdioParams`
- `augments.adk.mcp.MCPServerStreamableHttp`
- `augments.adk.mcp.MCPServerStreamableHttpParams`
- `augments.adk.mcp.MCPServerSse`
- `augments.adk.mcp.MCPServerSseParams`

## Lifecycle

- `augments.adk.mcp.MCPServerManager`

## Filters

- `augments.adk.mcp.ToolFilter`
- `augments.adk.mcp.ToolFilterContext`

## Auth and elicitation

- `augments.adk.mcp.HeaderProvider`
- `augments.adk.mcp.ElicitationHandler`

## Exceptions

- `augments.adk.mcp.MCPError`
- `augments.adk.mcp.MCPConnectionError`
- `augments.adk.mcp.MCPToolCallError`
- `augments.adk.mcp.MCPToolNotFoundError`
- `augments.adk.mcp.MCPSchemaConversionError`

The agent-facing adapter `MCPToolset` is a `Toolset` subclass and lives
under `augments.adk.tools.toolsets.mcp_toolset`. Usage lives in the
[MCP guide](../../mcp/mcp.md).
