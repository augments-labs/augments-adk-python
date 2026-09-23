# A2A

Agent-to-Agent protocol support: independent agents talking to each other
as peers, as protocol clients and as protocol servers.

The `a2a-sdk` package is an optional extra
(`pip install 'augments-adk[a2a]'`). When it is not installed,
every name below is bound to `None` so downstream code can skip A2A
wiring gracefully.

## Client side

- `augments.adk.a2a.A2AAgent`
- `augments.adk.a2a.A2ARunner`
- `augments.adk.a2a.A2AClient`
- `augments.adk.a2a.A2ARunResult`
- `augments.adk.a2a.A2AStreamEvent`

## Server side

- `augments.adk.a2a.A2AServer`
- `augments.adk.a2a.A2AExecutor`
- `augments.adk.a2a.build_starlette_app`

## Long-running tasks

- `augments.adk.a2a.A2AContinuationToken`
- `augments.adk.a2a.A2ATaskStatus`
- `augments.adk.a2a.A2ATaskStateLiteral`
- `augments.adk.a2a.TaskStore`
- `augments.adk.a2a.InMemoryTaskStore`
- `augments.adk.a2a.SQLiteTaskStore`

## Composition

- `augments.adk.a2a.A2AExecutableAdapter`

## Exceptions

- `augments.adk.a2a.A2AError`
- `augments.adk.a2a.A2AProtocolError`
- `augments.adk.a2a.A2ATransportError`
- `augments.adk.a2a.A2ATaskError`
- `augments.adk.a2a.A2ATaskCancelledError`
- `augments.adk.a2a.A2ATaskInterruptedError`

Usage lives in the [A2A guide](../../a2a/a2a.md).
