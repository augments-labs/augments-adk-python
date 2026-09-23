"""Deployment engine — artifact generation + active deploy via host CLIs.

``augments deploy init`` renders a Dockerfile and per-target manifests;
the ship commands build and deploy by driving the operator's installed
CLIs (docker / gcloud / kubectl / aws / helm) through the
``CommandRunner`` seam. No cloud SDK is imported — the deploy path
runs the same commands an operator would by hand, so it adds no runtime
dependencies. Everything here is stdlib + click only.
"""

from __future__ import annotations

from augments.adk.deploy.artifacts import write_artifacts
from augments.adk.deploy.commands import (
    CommandResult,
    CommandRunner,
    DeployCommandFailed,
    DeployToolMissing,
    RecordingRunner,
    SubprocessRunner,
    require_tool,
    run_checked,
)
from augments.adk.deploy.context import DeployContext
from augments.adk.deploy.targets import (
    TARGETS,
    AppRunnerTarget,
    CloudRunTarget,
    DeployTarget,
    DockerTarget,
    ECSTarget,
    GKETarget,
    HelmTarget,
    K8sTarget,
    LambdaTarget,
)

__all__ = [
    "TARGETS",
    "AppRunnerTarget",
    "CloudRunTarget",
    "CommandResult",
    "CommandRunner",
    "DeployCommandFailed",
    "DeployContext",
    "DeployTarget",
    "DeployToolMissing",
    "DockerTarget",
    "ECSTarget",
    "GKETarget",
    "HelmTarget",
    "K8sTarget",
    "LambdaTarget",
    "RecordingRunner",
    "SubprocessRunner",
    "require_tool",
    "run_checked",
    "write_artifacts",
]
