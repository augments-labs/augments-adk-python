"""Deploy targets and the registry ``deploy init`` dispatches on.

New targets register here so ``augments deploy init --target <key>``
discovers them. Each target's ``generate`` returns a complete, deployable
artifact set (container artifacts plus its orchestration manifests).
"""

from __future__ import annotations

from augments.adk.deploy.targets.apprunner import AppRunnerTarget
from augments.adk.deploy.targets.aws_lambda import LambdaTarget
from augments.adk.deploy.targets.base import DeployTarget
from augments.adk.deploy.targets.cloudrun import CloudRunTarget
from augments.adk.deploy.targets.docker import DockerTarget
from augments.adk.deploy.targets.ecs import ECSTarget
from augments.adk.deploy.targets.gke import GKETarget
from augments.adk.deploy.targets.helm import HelmTarget
from augments.adk.deploy.targets.k8s import K8sTarget

TARGETS: dict[str, DeployTarget] = {
    DockerTarget.key: DockerTarget(),
    K8sTarget.key: K8sTarget(),
    GKETarget.key: GKETarget(),
    HelmTarget.key: HelmTarget(),
    CloudRunTarget.key: CloudRunTarget(),
    ECSTarget.key: ECSTarget(),
    AppRunnerTarget.key: AppRunnerTarget(),
    LambdaTarget.key: LambdaTarget(),
}

__all__ = [
    "TARGETS",
    "AppRunnerTarget",
    "CloudRunTarget",
    "DeployTarget",
    "DockerTarget",
    "ECSTarget",
    "GKETarget",
    "HelmTarget",
    "K8sTarget",
    "LambdaTarget",
]
