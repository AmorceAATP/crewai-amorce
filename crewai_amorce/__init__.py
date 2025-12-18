"""
CrewAI-Amorce Integration

Secure CrewAI crews with Ed25519 signatures and HITL approvals.
Now with agent discovery via Amorce ANS!
"""

from crewai_amorce.decorators import secure_crew
from crewai_amorce.agent import SecureAgent
from crewai_amorce.discovery import (
    SearchAgentsTool,
    GetAgentTool,
    get_discovery_tools,
)

__version__ = "0.2.0"
__all__ = [
    "secure_crew",
    "SecureAgent",
    "SearchAgentsTool",
    "GetAgentTool",
    "get_discovery_tools",
]
