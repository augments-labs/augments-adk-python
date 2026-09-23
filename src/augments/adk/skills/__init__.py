"""Skills module — reusable capability packages for agents.

Skills combine domain instructions, tools, resources, and governance
into composable units that can be attached to agents.
"""

from augments.adk.skills.activation import SkillActivation
from augments.adk.skills.discovery import SkillDiscoveryToolset
from augments.adk.skills.skill import Skill, SkillGovernance, SkillMetadata
from augments.adk.skills.skill_prompt import (
    RECOMMENDED_SKILL_INSTRUCTIONS,
    prompt_with_skill_instructions,
)
from augments.adk.skills.skill_set import SkillSet

__all__ = [
    "RECOMMENDED_SKILL_INSTRUCTIONS",
    "Skill",
    "SkillActivation",
    "SkillDiscoveryToolset",
    "SkillGovernance",
    "SkillMetadata",
    "SkillSet",
    "prompt_with_skill_instructions",
]
