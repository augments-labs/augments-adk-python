"""Temporal.io durable execution backend for Augments ADK.

Wraps agent, graph, swarm, and flow runs as Temporal workflows with
crash-recovery, retry, and deterministic replay.

Install the ``temporal`` optional extra before importing this package::

    pip install "augments-adk[temporal]"

Public surface exported here covers configuration types, the LLM shim,
tool wrapping helpers, the HITL workflow base class, streaming, MCP
routing, and worker wiring.
"""

from __future__ import annotations

from augments.adk.workflows.engine import ModelActivityConfig, ToolActivityConfig
from augments.adk.workflows.temporal.llm import TemporalLLM
from augments.adk.workflows.temporal.mcp import TemporalMCPToolSet
from augments.adk.workflows.temporal.plugin import AugmentsTemporalPlugin
from augments.adk.workflows.temporal.routing import (
    MappingTaskQueueRouter,
    TenantTaskQueueRouter,
    start_tenant_workflow,
)
from augments.adk.workflows.temporal.streaming import TemporalStreamingLLM
from augments.adk.workflows.temporal.tools import TemporalToolWrapper, activity_tool, to_durable_tool
from augments.adk.workflows.temporal.tracing import (
    deterministic_timestamp,
    deterministic_uuid,
    should_emit_span,
)
from augments.adk.workflows.temporal.workflow import AugmentsWorkflow, HumanReply, ToolApprovalDecision

__all__ = [
    "AugmentsTemporalPlugin",
    "AugmentsWorkflow",
    "HumanReply",
    "MappingTaskQueueRouter",
    "ModelActivityConfig",
    "TemporalLLM",
    "TemporalMCPToolSet",
    "TemporalStreamingLLM",
    "TemporalToolWrapper",
    "TenantTaskQueueRouter",
    "ToolActivityConfig",
    "ToolApprovalDecision",
    "activity_tool",
    "deterministic_timestamp",
    "deterministic_uuid",
    "should_emit_span",
    "start_tenant_workflow",
    "to_durable_tool",
]
