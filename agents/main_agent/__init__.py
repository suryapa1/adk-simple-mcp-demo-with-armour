from .agent import customer_service_agent

# ADK expects the main agent to be named 'root_agent'
root_agent = customer_service_agent

__all__ = ["root_agent", "customer_service_agent"]

