# Graphs

State-machine orchestration: a directed graph of nodes executed in
supersteps, with checkpointing, interrupts, and streaming events.

## Core

- `augments.adk.graphs.Graph`
- `augments.adk.graphs.GraphBuilder`
- `augments.adk.graphs.GraphConfig`

## Nodes and edges

- `augments.adk.graphs.GraphNode`
- `augments.adk.graphs.GraphEdge`
- `augments.adk.graphs.EdgeCondition`
- `augments.adk.graphs.NodeInputStrategy`
- `augments.adk.graphs.NodeRetryPolicy`
- `augments.adk.graphs.prepare_node_input`

## State and results

- `augments.adk.graphs.GraphState`
- `augments.adk.graphs.GraphRunResult`
- `augments.adk.graphs.GraphRunResultStreaming`
- `augments.adk.graphs.GraphRunStatus`
- `augments.adk.graphs.StructuredInterrupts`

## Composition seam and adapters

- `augments.adk.graphs.Executable`
- `augments.adk.graphs.ExecutableInput`
- `augments.adk.graphs.NodeResult`
- `augments.adk.graphs.AgentExecutable`
- `augments.adk.graphs.SwarmExecutable`
- `augments.adk.graphs.CallableExecutable`
- `augments.adk.graphs.CallableNodeFn`
- `augments.adk.graphs.to_executable`

## Merge and join

- `augments.adk.graphs.Merge`
- `augments.adk.graphs.MergeFn`
- `augments.adk.graphs.DEFAULT_MERGE`
- `augments.adk.graphs.JoinBarrier`
- `augments.adk.graphs.JoinSemantics`

## Checkpointers

- `augments.adk.graphs.Checkpointer`
- `augments.adk.graphs.GraphCheckpoint`
- `augments.adk.graphs.InMemoryCheckpointer`
- `augments.adk.graphs.SQLiteCheckpointer`
- `augments.adk.graphs.TieredCheckpointer`

## Hooks

- `augments.adk.graphs.GraphHooks`
- `augments.adk.graphs.HookProvider`
- `augments.adk.graphs.HookRegistry`

## Interrupts and resume

- `augments.adk.graphs.Interrupt`
- `augments.adk.graphs.InterruptException`
- `augments.adk.graphs.GraphResume`
- `augments.adk.graphs.GraphResumeError`
- `augments.adk.graphs.NestedGraphInterrupt`
- `augments.adk.graphs.NestedAgentInterrupt`
- `augments.adk.graphs.NestedAgentApproval`
- `augments.adk.graphs.NestedAgentRejection`
- `augments.adk.graphs.NestedAgentReply`
- `augments.adk.graphs.NestedAgentDecision`
- `augments.adk.graphs.NestedAgentResumeError`
- `augments.adk.graphs.NestedAgentSerializationError`
- `augments.adk.graphs.request_human_input`
- `augments.adk.graphs.NESTED_AGENT_TOOL_APPROVAL_KIND`
- `augments.adk.graphs.NESTED_GRAPH_INTERRUPT_KIND`

## Events

- `augments.adk.graphs.GraphStreamEvent`
- `augments.adk.graphs.GraphEndEvent`
- `augments.adk.graphs.NodeStartEvent`
- `augments.adk.graphs.NodeEndEvent`
- `augments.adk.graphs.NodeErrorEvent`
- `augments.adk.graphs.NodeStreamEvent`
- `augments.adk.graphs.SuperstepStartEvent`
- `augments.adk.graphs.GRAPH_START`
- `augments.adk.graphs.GRAPH_END`
- `augments.adk.graphs.NODE_START`
- `augments.adk.graphs.NODE_END`
- `augments.adk.graphs.NODE_ERROR`
- `augments.adk.graphs.NODE_INTERRUPT`
- `augments.adk.graphs.NODE_STREAM`
- `augments.adk.graphs.SUPERSTEP_START`
- `augments.adk.graphs.SUPERSTEP_END`

Three further `GraphStreamEvent` subclasses, spelled out with the keys
each one carries:

- `GraphStartEvent` — emitted once at the top of a graph run, before
  the first superstep. Keys: `type` (always `GRAPH_START`),
  `graph_path`, `graph_id`, `description`, `entry_node`,
  `terminal_nodes`.
- `SuperstepEndEvent` — emitted after a superstep completes. Keys:
  `type` (always `SUPERSTEP_END`), `graph_path`, `superstep`,
  `fired_nodes`, `errored_nodes`.
- `NodeInterruptEvent` — a node raised `InterruptException` and the
  run is suspending; carries the pending `Interrupt` so consumers can
  prompt the human and resume via `GraphResume`. Keys: `type` (always
  `NODE_INTERRUPT`), `graph_path`, `node_id`, `interrupt`.

Graphs are executed via `Runner.arun_graph`. The end-to-end walkthrough
lives in the [Graphs guide](../../graphs/graphs.md).
