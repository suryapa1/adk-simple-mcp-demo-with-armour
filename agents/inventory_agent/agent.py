"""Inventory Agent - Uses Inventory MCP Server"""
from google.adk.agents import LlmAgent
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

# Create MCP toolset pointing to local inventory server
inventory_mcp = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python3.11",
            args=["/home/ubuntu/adk-simple-mcp-demo/mcp_servers/inventory/server.py"],
        )
    )
)

# Create inventory agent that uses MCP tools
inventory_agent = LlmAgent(
    name="inventory_agent",
    model="gemini-2.0-flash-exp",
    instruction="""You are an inventory specialist.
    
Your job is to check product stock levels and inventory status.

When asked about product availability:
1. Use check_stock tool to get current stock
2. Provide clear stock status
3. Mention if product is in stock or out of stock

When asked about low stock:
1. Use get_low_stock_products tool
2. List products that need restocking

Always be concise and factual.""",
    tools=[inventory_mcp],
)

