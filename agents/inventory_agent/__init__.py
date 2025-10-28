from .agent import inventory_agent

# ADK expects the main agent to be named 'root_agent'
root_agent = inventory_agent

__all__ = ["root_agent", "inventory_agent"]
