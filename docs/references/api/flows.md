# Flows

Decorator-driven multi-step orchestration over typed shared state, with
event-driven listeners and state-based routers.

## Core

- `augments.adk.flows.Flow`
- `augments.adk.flows.FlowMeta`
- `augments.adk.flows.FlowStep`
- `augments.adk.flows.FlowRole`

## Decorators

- `augments.adk.flows.flow_start`
- `augments.adk.flows.flow_listen`
- `augments.adk.flows.flow_router`
- `augments.adk.flows.FlowTriggerSpec`

## Combinators

- `augments.adk.flows.Or`
- `augments.adk.flows.And`

## Config and results

- `augments.adk.flows.FlowConfig`
- `augments.adk.flows.FlowErrorPolicy`
- `augments.adk.flows.FlowRunResult`
- `augments.adk.flows.FlowRunResultStreaming`
- `augments.adk.flows.FlowRunStatus`

## Triggers

- `augments.adk.flows.FlowTriggerEvent`
- `augments.adk.flows.FlowTriggerKind`
- `augments.adk.flows.FLOW_ERROR_TRIGGER`

## Events

- `augments.adk.flows.FlowStartEvent`
- `augments.adk.flows.FlowEndEvent`
- `augments.adk.flows.FlowStepStartEvent`
- `augments.adk.flows.FlowStepEndEvent`
- `augments.adk.flows.FlowStepErrorEvent`
- `augments.adk.flows.FlowStepSkippedEvent`
- `augments.adk.flows.FlowStepDeferredEvent`
- `augments.adk.flows.FlowStepRejectedEvent`
- `augments.adk.flows.FlowRouteEvaluatedEvent`
- `augments.adk.flows.FlowEvent`

## Approvals and deferral

- `augments.adk.flows.FlowApprovalPolicy`
- `augments.adk.flows.FlowApprovalDecision`
- `augments.adk.flows.FlowApprovalStatus`
- `augments.adk.flows.FlowDeferralKind`
- `augments.adk.flows.FlowDeferredStep`
- `augments.adk.flows.FlowAgentDeferred`

## Step governance

- `augments.adk.flows.FlowStepContext`
- `augments.adk.flows.FlowStepGate`
- `augments.adk.flows.FlowStepGuardrails`
- `augments.adk.flows.FlowStepGuardrailFn`
- `augments.adk.flows.FlowStepGuardrailVerdict`
- `augments.adk.flows.FlowStepCachePolicy`
- `augments.adk.flows.FlowCacheKeyFn`
- `augments.adk.flows.FlowStepRateLimit`
- `augments.adk.flows.FlowStepRateLimitBehavior`

## Persistence and distributed execution

- `augments.adk.flows.FlowCheckpoint`
- `augments.adk.flows.FlowWorkerBackend`
- `augments.adk.flows.FlowBatchClaim`
- `augments.adk.flows.InMemoryFlowWorkerBackend`
- `augments.adk.flows.SqliteFlowWorkerBackend`

## Definition and registry

- `augments.adk.flows.FlowDefinition`
- `augments.adk.flows.StepInfo`
- `augments.adk.flows.GateInfo`
- `augments.adk.flows.FlowStepRegistry`
- `augments.adk.flows.FlowTransitionTable`
- `augments.adk.flows.GateSpec`
- `augments.adk.flows.TriggerSpec`
- `augments.adk.flows.build_flow_definition`
- `augments.adk.flows.build_transition_table`
- `augments.adk.flows.collect_step_descriptions`

## Agent bridge

- `augments.adk.flows.FlowExecutable`
- `augments.adk.flows.arun_flow_agent`

## Exceptions

- `augments.adk.flows.FlowDefinitionError`
- `augments.adk.flows.FlowStepError`
- `augments.adk.flows.FlowMaxStepsExceeded`
- `augments.adk.flows.FlowCheckpointNotFoundError`

Flows are executed via `Runner.arun_flow`. The end-to-end walkthrough
lives in the [Flows guide](../../flows/flows.md).
