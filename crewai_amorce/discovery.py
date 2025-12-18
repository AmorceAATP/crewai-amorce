"""
Amorce Discovery Tools for CrewAI

Enables CrewAI crews to discover other AI agents via Amorce ANS.
"""

from typing import Optional, List, Any
import requests


class SearchAgentsTool:
    """
    CrewAI tool to search for AI agents via Amorce ANS.
    
    Use this to find specialized agents for specific tasks.
    """
    
    name = "search_agents"
    description = (
        "Search for AI agents that can help with a specific task. "
        "Input should be a natural language description of what you need, "
        "e.g., 'book flights to Paris' or 'check weather forecast'. "
        "Returns a list of agents with their capabilities and trust scores."
    )
    
    def __init__(self, trust_url: Optional[str] = None):
        self.trust_url = trust_url or "https://amorce-trust-api-425870997313.us-central1.run.app"
    
    def run(self, query: str) -> str:
        """Search for agents matching the query."""
        try:
            response = requests.get(
                f"{self.trust_url}/api/v1/ans/search",
                params={"q": query, "limit": 5}
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get("results"):
                return "No agents found for this query."
            
            # Format results
            results = []
            for i, agent in enumerate(data["results"][:5], 1):
                results.append(
                    f"{i}. {agent['name']} (Trust: {agent['trust_score']})\n"
                    f"   Category: {agent.get('category', 'N/A')}\n"
                    f"   ID: {agent['agent_id']}"
                )
            
            return f"Found {len(data['results'])} agents:\n\n" + "\n\n".join(results)
            
        except Exception as e:
            return f"Error searching agents: {str(e)}"
    
    def __call__(self, query: str) -> str:
        return self.run(query)


class GetAgentTool:
    """
    CrewAI tool to get details about a specific agent.
    """
    
    name = "get_agent"
    description = (
        "Get detailed information about a specific AI agent. "
        "Input should be the agent_id from search results."
    )
    
    def __init__(self, trust_url: Optional[str] = None):
        self.trust_url = trust_url or "https://amorce-trust-api-425870997313.us-central1.run.app"
    
    def run(self, agent_id: str) -> str:
        """Get agent details."""
        try:
            response = requests.get(f"{self.trust_url}/api/v1/agents/{agent_id}")
            response.raise_for_status()
            agent = response.json()
            
            return (
                f"Name: {agent.get('name', 'Unknown')}\n"
                f"ID: {agent.get('agent_id')}\n"
                f"Category: {agent.get('category', 'N/A')}\n"
                f"Description: {agent.get('description', 'No description')}\n"
                f"Endpoint: {agent.get('endpoint', 'N/A')}\n"
                f"Capabilities: {', '.join(agent.get('capabilities', [])) or 'N/A'}\n"
                f"Trust Score: {agent.get('trust_score', 'N/A')}"
            )
            
        except Exception as e:
            return f"Error getting agent: {str(e)}"
    
    def __call__(self, agent_id: str) -> str:
        return self.run(agent_id)


def get_discovery_tools(trust_url: Optional[str] = None) -> List[Any]:
    """
    Get all Amorce discovery tools for CrewAI.
    
    Returns:
        List of tools: [SearchAgentsTool, GetAgentTool]
    """
    return [
        SearchAgentsTool(trust_url),
        GetAgentTool(trust_url),
    ]
