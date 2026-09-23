"""Flow primitive — decorator-driven multi-step orchestration over typed shared state.

A ``Flow`` is a class-based, declarative orchestration that composes
``Agent``, ``Swarm``,
``Graph``, and ``Task``
calls as ordered steps, with typed shared state, event-driven listeners,
and state-based routers. Fills the gap between the existing
``Graph`` (DAG with message-threading) and
``TaskPipeline`` (sequential with no
typed shared state).

Canonical minimal example — a two-step Flow over a Pydantic state::

    from pydantic import BaseModel

    from augments.adk import Runner
    from augments.adk.flows import Flow, flow_listen, flow_start


    class ResearchState(BaseModel):
        topic: str = ""
        summary: str = ""


    class ResearchFlow(Flow[ResearchState]):
        state_factory = ResearchState

        @flow_start
        async def kickoff(self) -> None:
            self.state.topic = "climate"

        @flow_listen(kickoff)
        async def summarize(self) -> None:
            self.state.summary = f"Summary of {self.state.topic}."


    flow = ResearchFlow()  # or ResearchFlow(initial_state=ResearchState(topic="ml"))
    result = await Runner.arun_flow(flow)

**Anti-hidden-behavior contract**: every wire is declared by an explicit
decorator on a method; step methods take only ``self``; ``self.state`` is
the developer's mutable typed object; persistence is explicit via
``FlowCheckpoint``. The framework
NEVER auto-injects arguments, auto-persists state, auto-routes on bare
string returns, or auto-instantiates state from the generic parameter.

**Combinators are operator-only**: use ``method_a | method_b`` /
``method_a & method_b``. There are no ``or_()`` / ``and_()`` helper
functions in this ADK — those CrewAI helpers are intentionally omitted
in favor of the fluent operator API.

The name ``Flow`` (rather than ``Workflow``) reserves the latter name
for the future Temporal-style durable execution layer, which composes
*over* this orchestration topology.

See ``docs/flows/flows.md`` for usage and ``examples/flows/`` for runnable
examples.
"""

from __future__ import annotations

from augments.adk.flows.agent_bridge import arun_flow_agent
from augments.adk.flows.approval_policy import FlowApprovalPolicy
from augments.adk.flows.checkpoint import FlowCheckpoint
from augments.adk.flows.combinators import And, Or
from augments.adk.flows.config import FlowConfig, FlowErrorPolicy
from augments.adk.flows.decorators import FlowTriggerSpec, flow_listen, flow_router, flow_start
from augments.adk.flows.deferred import (
    FlowApprovalDecision,
    FlowApprovalStatus,
    FlowDeferralKind,
    FlowDeferredStep,
)
from augments.adk.flows.definition import (
    FlowDefinition,
    GateInfo,
    StepInfo,
    build_flow_definition,
)
from augments.adk.flows.events import (
    FlowEndEvent,
    FlowEvent,
    FlowRouteEvaluatedEvent,
    FlowStartEvent,
    FlowStepDeferredEvent,
    FlowStepEndEvent,
    FlowStepErrorEvent,
    FlowStepRejectedEvent,
    FlowStepSkippedEvent,
    FlowStepStartEvent,
)
from augments.adk.flows.exceptions import (
    FlowAgentDeferred,
    FlowCheckpointNotFoundError,
    FlowDefinitionError,
    FlowMaxStepsExceeded,
    FlowStepError,
)
from augments.adk.flows.executable import FlowExecutable
from augments.adk.flows.flow import Flow, FlowMeta, collect_step_descriptions
from augments.adk.flows.flow_wrappers import FlowRole, FlowStep
from augments.adk.flows.registry import (
    FlowStepRegistry,
    FlowTransitionTable,
    GateSpec,
    TriggerSpec,
    build_transition_table,
)
from augments.adk.flows.result import FlowRunResult, FlowRunResultStreaming, FlowRunStatus
from augments.adk.flows.sqlite_worker_backend import SqliteFlowWorkerBackend
from augments.adk.flows.step_cache_policy import FlowCacheKeyFn, FlowStepCachePolicy
from augments.adk.flows.step_context import FlowStepContext, FlowStepGate
from augments.adk.flows.step_guardrails import (
    FlowStepGuardrailFn,
    FlowStepGuardrails,
    FlowStepGuardrailVerdict,
)
from augments.adk.flows.step_rate_limit import (
    FlowStepRateLimit,
    FlowStepRateLimitBehavior,
)
from augments.adk.flows.triggers import FLOW_ERROR_TRIGGER, FlowTriggerEvent, FlowTriggerKind
from augments.adk.flows.worker_backend import (
    FlowBatchClaim,
    FlowWorkerBackend,
    InMemoryFlowWorkerBackend,
)

__all__ = [
    # Alphabetically sorted (RUF022). Themes, for orientation:
    # core (Flow, FlowStep), decorators (flow_*), combinators (Or, And),
    # config & result, events, HITL & deferral, step governance,
    # triggers, distributed execution, exceptions, definition/registry.
    "FLOW_ERROR_TRIGGER",
    "And",
    "Flow",
    "FlowAgentDeferred",
    "FlowApprovalDecision",
    "FlowApprovalPolicy",
    "FlowApprovalStatus",
    "FlowBatchClaim",
    "FlowCacheKeyFn",
    "FlowCheckpoint",
    "FlowCheckpointNotFoundError",
    "FlowConfig",
    "FlowDeferralKind",
    "FlowDeferredStep",
    "FlowDefinition",
    "FlowDefinitionError",
    "FlowEndEvent",
    "FlowErrorPolicy",
    "FlowEvent",
    "FlowExecutable",
    "FlowMaxStepsExceeded",
    "FlowMeta",
    "FlowRole",
    "FlowRouteEvaluatedEvent",
    "FlowRunResult",
    "FlowRunResultStreaming",
    "FlowRunStatus",
    "FlowStartEvent",
    "FlowStep",
    "FlowStepCachePolicy",
    "FlowStepContext",
    "FlowStepDeferredEvent",
    "FlowStepEndEvent",
    "FlowStepError",
    "FlowStepErrorEvent",
    "FlowStepGate",
    "FlowStepGuardrailFn",
    "FlowStepGuardrailVerdict",
    "FlowStepGuardrails",
    "FlowStepRateLimit",
    "FlowStepRateLimitBehavior",
    "FlowStepRegistry",
    "FlowStepRejectedEvent",
    "FlowStepSkippedEvent",
    "FlowStepStartEvent",
    "FlowTransitionTable",
    "FlowTriggerEvent",
    "FlowTriggerKind",
    "FlowTriggerSpec",
    "FlowWorkerBackend",
    "GateInfo",
    "GateSpec",
    "InMemoryFlowWorkerBackend",
    "Or",
    "SqliteFlowWorkerBackend",
    "StepInfo",
    "TriggerSpec",
    "arun_flow_agent",
    "build_flow_definition",
    "build_transition_table",
    "collect_step_descriptions",
    "flow_listen",
    "flow_router",
    "flow_start",
]
