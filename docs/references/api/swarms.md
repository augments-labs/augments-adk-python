# Swarms

Multi-agent iterative collaboration: a roster of agents taking turns on a
shared problem until an explicit termination signal fires.

## Core

- `augments.adk.swarms.Swarm`
- `augments.adk.swarms.SwarmBuilder`
- `augments.adk.swarms.SwarmConfig`

## Policies

- `augments.adk.swarms.SwarmPolicy`
- `augments.adk.swarms.LLMHandoffPolicy`
- `augments.adk.swarms.RoundRobinPolicy`
- `augments.adk.swarms.StructuredRoutingPolicy`
- `augments.adk.swarms.CustomPolicy`
- `augments.adk.swarms.SwarmSelector`
- `augments.adk.swarms.SwarmExtraToolsFn`

## Termination

- `augments.adk.swarms.TerminationCondition`
- `augments.adk.swarms.ExplicitDoneTermination`
- `augments.adk.swarms.MaxTurnsTermination`
- `augments.adk.swarms.TokenBudgetTermination`
- `augments.adk.swarms.TextMentionTermination`
- `augments.adk.swarms.HandoffToTermination`
- `augments.adk.swarms.AndTermination`
- `augments.adk.swarms.OrTermination`

## State and results

- `augments.adk.swarms.SwarmState`
- `augments.adk.swarms.SwarmStateDict`
- `augments.adk.swarms.SwarmRunResult`
- `augments.adk.swarms.SwarmRunResultStreaming`
- `augments.adk.swarms.StopReason`

## Events

- `augments.adk.swarms.SwarmStartEvent`
- `augments.adk.swarms.SwarmTurnStartEvent`
- `augments.adk.swarms.SwarmTurnEndEvent`
- `augments.adk.swarms.SwarmTurnInterruptEvent`
- `augments.adk.swarms.SwarmHandoffEvent`
- `augments.adk.swarms.SwarmDoneEvent`
- `augments.adk.swarms.SwarmEvent`

## Yield signals

- `augments.adk.swarms.SwarmDone`
- `augments.adk.swarms.SwarmHandoff`
- `augments.adk.swarms.SwarmYieldSignal`

## Hooks and checkpoints

- `augments.adk.swarms.SwarmHooks`
- `augments.adk.swarms.HookRegistry`
- `augments.adk.swarms.SwarmHookRegistry`
- `augments.adk.swarms.SwarmCheckpoint`
- `augments.adk.swarms.SwarmCheckpointer`

## Interrupt and resume

- `augments.adk.swarms.SwarmResume`
- `augments.adk.swarms.request_human_input_in_swarm`

## Shared context

- `augments.adk.swarms.SharedContextConfig`
- `augments.adk.swarms.SharedContextStrategy`
- `augments.adk.swarms.prepare_turn_input`
- `augments.adk.swarms.prompt_with_swarm_instructions`

## Constants

- `augments.adk.swarms.DEFAULT_MAX_TURNS`
- `augments.adk.swarms.DEFAULT_TERMINATION`
- `augments.adk.swarms.RECOMMENDED_SWARM_PROMPT_PREFIX`
- `augments.adk.swarms.SWARM_DONE_TOOL_NAME`

Swarms are executed via `Runner.arun_swarm`. The end-to-end walkthrough
lives in the [Swarms guide](../../swarms/swarms.md).
