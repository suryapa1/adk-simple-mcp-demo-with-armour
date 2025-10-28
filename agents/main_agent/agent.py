"""Main Customer Service Agent"""
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

# Import sub-agents
import sys
sys.path.append('/home/ubuntu/adk-simple-mcp-demo/agents')
from inventory_agent.agent import inventory_agent
from shipping_agent.agent import shipping_agent

# Direct tools for main agent
def get_store_hours() -> dict:
    """Get store operating hours
    
    Returns:
        Store hours information
    """
    return {
        "online_store": "24/7",
        "customer_service": "9 AM - 6 PM EST, Monday-Friday",
        "phone": "1-800-EXAMPLE"
    }

def get_return_policy() -> dict:
    """Get return policy information
    
    Returns:
        Return policy details
    """
    return {
        "return_window": "30 days",
        "condition": "Unopened and unused",
        "refund_method": "Original payment method",
        "restocking_fee": "None for defective items, 15% for other returns"
    }

# Wrap sub-agents as tools
inventory_tool = AgentTool(agent=inventory_agent)
shipping_tool = AgentTool(agent=shipping_agent)

# Create main agent
customer_service_agent = LlmAgent(
    name="customer_service",
    model="gemini-2.0-flash-exp",
    instruction="""You are a helpful customer service representative.

You can help customers with:
1. Store hours and contact information (use get_store_hours)
2. Return policy questions (use get_return_policy)
3. Product inventory and stock (use inventory_agent)
4. Shipment tracking (use shipping_agent)

When a customer asks:
- About store hours or contact → use get_store_hours
- About returns or refunds → use get_return_policy
- About product availability or stock → use inventory_agent
- About shipment status or tracking → use shipping_agent

Always be friendly, professional, and helpful.""",
    tools=[
        get_store_hours,
        get_return_policy,
        inventory_tool,
        shipping_tool,
    ],
)

