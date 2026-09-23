# Types

Provider-agnostic wire and history types shared across the framework.

## Run items

- `augments.adk.types.RunItem`
- `augments.adk.types.RunItemBase`
- `augments.adk.types.UserItem`
- `augments.adk.types.SystemItem`
- `augments.adk.types.MessageOutputItem`
- `augments.adk.types.ReasoningItem`
- `augments.adk.types.ToolCallItem`
- `augments.adk.types.ToolCallOutputItem`
- `augments.adk.types.ToolApprovalItem`
- `augments.adk.types.ToolSearchCallItem`
- `augments.adk.types.ToolSearchOutputItem`
- `augments.adk.types.HandoffCallItem`
- `augments.adk.types.HandoffOutputItem`
- `augments.adk.types.MCPListToolsItem`
- `augments.adk.types.MCPApprovalRequestItem`
- `augments.adk.types.MCPApprovalResponseItem`
- `augments.adk.types.CompactionItem`
- `augments.adk.types.ItemHelpers`

## Result

### `augments.adk.types.RunResult`

Result of a completed (or interrupted) agent run. Contains the final
output (if the run completed), all items generated during execution,
and supports HITL interruptions via `deferred_requests`.

Fields:

- `final_output` — the final output from the agent, or `None` if
  interrupted for approval.
- `user_prompt` — the original user prompt passed to the run.
- `new_items` — Layer 3 `RunItem` values generated during this run
  (messages, tool calls, results).
- `context` — the run context with usage tracking.
- `last_agent` — the last agent that was active.
- `recovered` — `True` when an error handler produced `final_output`
  after the run raised; recovered runs skip session and memory
  persistence.
- `deferred_requests` — tools captured for approval or external
  execution; `None` if the run completed.
- `state` — serializable state for resuming interrupted runs.
- `guardrail_results` — per-phase agent-level guardrail audit trail
  (`input` and `output` slots).
- `guardrail_audit` — per-action guardrail audit records across every
  level (agent, tool, flow), captured as hashes, never raw payloads.
- `swarm_yield` — set only by the swarm driver when an agent turn
  yielded control; `None` on every plain `Runner.arun()` path.
- `sandbox_usage` — aggregate sandbox resource and cost usage, or
  `None` when no sandbox session ran.

Members:

- `requires_action` — property; `True` when human approval or external
  action is pending.
- `interruptions` — property; tool calls awaiting human approval, as a
  flat list.
- `last_response_id` — property; the `response_id` of the most recent
  LLM response in this run, or `None`.
- `release_agents(*, release_new_items=True)` — drop strong references
  to agents and, optionally, run items.
- `to_input_list()` — convert to a Layer 1 input list for a continued
  conversation.
- `final_output_as(output_type)` — cast the final output to the
  expected type.

Example:

```python
result = await Runner.arun(agent, "Delete user 123")
if result.requires_action:
    for req in list(result.deferred_requests.approvals):
        if await confirm(f"Approve {req.tool_name}?"):
            result.state.approve(req)
        else:
            result.state.reject(req, "Denied")
    result = await Runner.arun(agent, result.state)
```

## Built-in tool call and result types

- `augments.adk.types.WebSearchToolCall`
- `augments.adk.types.WebSearchToolCallResult`
- `augments.adk.types.WebSearchResult`
- `augments.adk.types.FileSearchToolCall`
- `augments.adk.types.FileSearchToolCallResult`
- `augments.adk.types.FileSearchResult`
- `augments.adk.types.CodeInterpreterToolCall`
- `augments.adk.types.CodeInterpreterToolCallResult`
- `augments.adk.types.CodeInterpreterOutput`
- `augments.adk.types.ComputerToolCall`
- `augments.adk.types.ComputerToolCallResult`
- `augments.adk.types.ComputerAction`
- `augments.adk.types.ImageGenerationToolCall`
- `augments.adk.types.ImageGenerationToolCallResult`
- `augments.adk.types.ShellToolCall`
- `augments.adk.types.ShellToolCallResult`
- `augments.adk.types.ApplyPatchToolCall`
- `augments.adk.types.ApplyPatchToolCallResult`
- `augments.adk.types.ToolSearchToolCall`
- `augments.adk.types.ToolSearchToolCallResult`
- `augments.adk.types.ToolSearchResultEntry`
- `augments.adk.types.MCPListTools`
- `augments.adk.types.MCPListToolsTool`
- `augments.adk.types.MCPCall`
- `augments.adk.types.MCPCallResult`
- `augments.adk.types.MCPApprovalRequest`
- `augments.adk.types.MCPApprovalResponse`

## Tracing span data

- `augments.adk.types.SpanData`
- `augments.adk.types.AgentSpanData`
- `augments.adk.types.FunctionSpanData`
- `augments.adk.types.GenerationSpanData`
- `augments.adk.types.GuardrailSpanData`
- `augments.adk.types.HandoffSpanData`
- `augments.adk.types.ResponseSpanData`
- `augments.adk.types.CustomSpanData`
- `augments.adk.types.AnySpanData`

How the type layers fit together is explained in the
[Types guide](../../types/types.md).
