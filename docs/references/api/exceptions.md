# Exceptions

The framework exception hierarchy. Every exception derives from
`AugmentsError`, so a single `except AugmentsError` catches all
framework-raised failures.

## Base

- `augments.adk.exceptions.AugmentsError`

## Concrete exceptions

- `augments.adk.exceptions.AgentInputGuardrailTripwireTriggered`
- `augments.adk.exceptions.AgentOutputGuardrailTripwireTriggered`
- `augments.adk.exceptions.AgentToolDeferral`
- `augments.adk.exceptions.ApplyPatchError`
- `augments.adk.exceptions.CheckpointConflictError`
- `augments.adk.exceptions.ConfigError`
- `augments.adk.exceptions.ConfigParseError`
- `augments.adk.exceptions.ConfigResolutionError`
- `augments.adk.exceptions.DocumentLoadError`
- `augments.adk.exceptions.ExecFailureError`
- `augments.adk.exceptions.ExecNonZeroError`
- `augments.adk.exceptions.ExecTimeoutError`
- `augments.adk.exceptions.ExecTransportError`
- `augments.adk.exceptions.ExposedPortUnavailableError`
- `augments.adk.exceptions.GitArtifactError`
- `augments.adk.exceptions.GraphNodeTimeoutError`
- `augments.adk.exceptions.GuardrailTripwireTriggered`
- `augments.adk.exceptions.HandoffDefinitionError`
- `augments.adk.exceptions.HandoffRejection`
- `augments.adk.exceptions.InvalidCompressionSchemeError`
- `augments.adk.exceptions.InvalidManifestPathError`
- `augments.adk.exceptions.LocalArtifactError`
- `augments.adk.exceptions.MaxTurnsExceeded`
- `augments.adk.exceptions.MemoryExtractionError`
- `augments.adk.exceptions.ModelRefusalError`
- `augments.adk.exceptions.MountArtifactError`
- `augments.adk.exceptions.NoRoutingCandidateError`
- `augments.adk.exceptions.NodeRetriesExhaustedError`
- `augments.adk.exceptions.PtySessionNotFoundError`
- `augments.adk.exceptions.QuotaExceeded`
- `augments.adk.exceptions.SandboxArtifactError`
- `augments.adk.exceptions.SandboxCommandRejected`
- `augments.adk.exceptions.SandboxConcurrencyError`
- `augments.adk.exceptions.SandboxConfigurationError`
- `augments.adk.exceptions.SandboxError`
- `augments.adk.exceptions.SandboxNetworkPolicyViolation`
- `augments.adk.exceptions.SandboxResourceLimitExceeded`
- `augments.adk.exceptions.SandboxRuntimeError`
- `augments.adk.exceptions.SandboxSelectionError`
- `augments.adk.exceptions.SandboxStartFailed`
- `augments.adk.exceptions.SandboxStopFailed`
- `augments.adk.exceptions.SessionAppendConflictError`
- `augments.adk.exceptions.SkillsConfigError`
- `augments.adk.exceptions.SnapshotError`
- `augments.adk.exceptions.SnapshotNotRestorableError`
- `augments.adk.exceptions.SnapshotPersistError`
- `augments.adk.exceptions.SnapshotRestoreError`
- `augments.adk.exceptions.TenantBudgetExceeded`
- `augments.adk.exceptions.ToolDependencyError`
- `augments.adk.exceptions.ToolGuardrailTripwireTriggered`
- `augments.adk.exceptions.ToolNotPermittedForTenant`
- `augments.adk.exceptions.ToolRetry`
- `augments.adk.exceptions.ToolTimeoutError`
- `augments.adk.exceptions.ToolsetNameConflictError`
- `augments.adk.exceptions.TracingDependencyError`
- `augments.adk.exceptions.UnsupportedDocumentSourceError`
- `augments.adk.exceptions.UnsupportedManifestEntryError`
- `augments.adk.exceptions.UnsupportedMountPatternError`
- `augments.adk.exceptions.UnsupportedMountStrategyError`
- `augments.adk.exceptions.UnsupportedSandboxClientError`
- `augments.adk.exceptions.UnsupportedSnapshotFeatureError`
- `augments.adk.exceptions.UsageLimitExceeded`
- `augments.adk.exceptions.UserError`
- `augments.adk.exceptions.WorkspaceArchiveReadError`
- `augments.adk.exceptions.WorkspaceArchiveWriteError`
- `augments.adk.exceptions.WorkspaceIOError`
- `augments.adk.exceptions.WorkspaceReadNotFoundError`

Domain-specific exceptions also live next to their modules — see
[Flows](flows.md) (flow execution), [MCP](mcp.md),
and [A2A](a2a.md).
