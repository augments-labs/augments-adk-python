"""Restate durable execution backend for Augments ADK.

Alternative to the Temporal backend using Restate's journaling-based
durable execution model.  LLM calls and tool calls are routed through
``ctx.run()`` so that results are journaled and replay-safe.

Install the ``restate`` optional extra before importing this package::

    pip install "augments-adk[restate]"
"""

from __future__ import annotations

from augments.adk.workflows.restate.llm import RestateLLM
from augments.adk.workflows.restate.service import AugmentsRestateService, RestateHumanReply
from augments.adk.workflows.restate.tools import restate_tool

__all__ = [
    "AugmentsRestateService",
    "RestateHumanReply",
    "RestateLLM",
    "restate_tool",
]
