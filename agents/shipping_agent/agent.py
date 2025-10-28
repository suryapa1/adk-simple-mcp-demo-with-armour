"""Shipping Agent - Uses Shipping MCP Server"""
from google.adk.agents import LlmAgent
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

# Create MCP toolset pointing to local shipping server
shipping_mcp = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python3.11",
            args=["/home/ubuntu/adk-simple-mcp-demo/mcp_servers/shipping/server.py"],
        )
    )
)

# Create shipping agent that uses MCP tools
shipping_agent = LlmAgent(
    name="shipping_agent",
    model="gemini-2.0-flash-exp",
    instruction="""You are a shipping specialist.

Your job is to track shipments and provide delivery status.

When asked about a specific shipment:
1. Use track_shipment tool with the tracking number
2. Provide status and current location
3. Be clear about delivery status

When asked about active shipments:
1. Use get_active_shipments tool
2. List all non-delivered shipments

Always be helpful and provide accurate tracking information.""",
    tools=[shipping_mcp],
)
