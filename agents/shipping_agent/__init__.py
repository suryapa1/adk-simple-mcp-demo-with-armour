from .agent import shipping_agent

# ADK expects the main agent to be named 'root_agent'
root_agent = shipping_agent

__all__ = ["root_agent", "shipping_agent"]
