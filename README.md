# Simple Multi-Agent MCP Demo

## Architecture

```
Main Agent (customer_service)
├─→ Direct Tool: get_store_hours()
├─→ Direct Tool: get_return_policy()
├─→ AgentTool: inventory_agent
│   └─→ MCPToolset: inventory_mcp
│       ├─→ check_stock(product_id)
│       └─→ get_low_stock_products(threshold)
└─→ AgentTool: shipping_agent
    └─→ MCPToolset: shipping_mcp
        ├─→ track_shipment(tracking_number)
        └─→ get_active_shipments()
```

## Complete Lineage Example

When you ask: **"Is PROD-001 in stock?"**

```
Main Agent (customer_service)
└─ execute_tool inventory_agent ✅
   └─ Agent: inventory_agent
      └─ execute_tool check_stock ✅
         └─ MCP Server: Inventory Service
            └─ Returns: {"product_id": "PROD-001", "stock": 45, "in_stock": true}
```

## Components

### 1. MCP Servers (FastMCP)
- **inventory/server.py** - 2 tools (check_stock, get_low_stock_products)
- **shipping/server.py** - 2 tools (track_shipment, get_active_shipments)

### 2. Sub-Agents (Use MCP Tools)
- **inventory_agent** - Uses inventory MCP tools
- **shipping_agent** - Uses shipping MCP tools

### 3. Main Agent (Uses Sub-Agents as Tools)
- **customer_service** - Has 2 direct tools + 2 agent tools

## Quick Start

### 1. Install Dependencies
```bash
pip install google-adk fastmcp
```

### 2. Run ADK Web UI
```bash
cd /home/ubuntu/adk-simple-mcp-demo
export GOOGLE_API_KEY=your-key
adk web --host 0.0.0.0 --port 8004 agents/main_agent
```

### 3. Test Queries

**Direct Tool (No Sub-Agent):**
- "What are your store hours?"
- "What is your return policy?"

**Inventory Agent (MCP Tools):**
- "Is PROD-001 in stock?"
- "Check stock for PROD-002"
- "Show me low stock products"

**Shipping Agent (MCP Tools):**
- "Track shipment SHIP-001"
- "Where is SHIP-002?"
- "Show active shipments"

## Expected Lineage

### Query: "Is PROD-001 in stock?"

**Trace View:**
```
invocation
└─ agent_run [customer_service]
   ├─ call_llm
   └─ execute_tool inventory_agent
      └─ invocation
         └─ agent_run [inventory_agent]
            ├─ call_llm
            └─ execute_tool check_stock
               └─ MCP call to Inventory Service
            └─ call_llm
   └─ call_llm
```

## Key Points

1. ✅ **MCP tools are NOT directly used by main agent**
2. ✅ **Sub-agents use MCP tools internally**
3. ✅ **Sub-agents are wrapped as AgentTool**
4. ✅ **Main agent calls AgentTool (which runs sub-agent)**
5. ✅ **Complete lineage visible in Trace tab**

## Sample Data

### Inventory
- PROD-001: Laptop Pro 15 (45 in stock)
- PROD-002: Wireless Mouse (120 in stock)
- PROD-003: USB-C Cable (200 in stock)
- PROD-004: Monitor 27in (15 in stock - LOW!)

### Shipments
- SHIP-001: Delivered
- SHIP-002: In Transit (Chicago)
- SHIP-003: Processing (Seattle)

## Troubleshooting

### MCP Server Not Starting
- Check that fastmcp is installed
- Verify Python path in MCPToolset server_args

### Agent Not Found
- Ensure __init__.py files exist
- Check import paths in main_agent/agent.py

### No Tools Showing
- Verify MCP server is running
- Check MCPToolset configuration
- Look for errors in ADK logs

## Next Steps

1. Test all query types
2. Observe lineage in Trace tab
3. Add more MCP tools
4. Deploy to Agent Engine

