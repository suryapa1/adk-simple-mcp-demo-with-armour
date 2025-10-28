# Multi-Agent MCP Architecture - Complete Guide

## What You Asked For

You wanted to understand:
1. **Where MCP server tools are used**
2. **How sub-agents relate to main agent**
3. **Complete lineage visibility**

## Answer: How It Works

### MCP Tools Are NOT Directly Used by Main Agent

```
❌ WRONG:
Main Agent → MCP Tool (FastMCP server)

✅ CORRECT:
Main Agent → AgentTool (sub-agent) → MCP Tool (FastMCP server)
```

### Complete Architecture

```
Main Agent (customer_service)
│
├─→ Direct Python Tool: get_store_hours()
│   └─→ Returns dict directly
│
├─→ Direct Python Tool: get_return_policy()
│   └─→ Returns dict directly
│
├─→ AgentTool: inventory_agent ⭐
│   └─→ Sub-Agent: inventory_agent
│       └─→ MCPToolset: inventory_mcp
│           ├─→ MCP Tool: check_stock()
│           │   └─→ FastMCP Server (Inventory Service)
│           └─→ MCP Tool: get_low_stock_products()
│               └─→ FastMCP Server (Inventory Service)
│
└─→ AgentTool: shipping_agent ⭐
    └─→ Sub-Agent: shipping_agent
        └─→ MCPToolset: shipping_mcp
            ├─→ MCP Tool: track_shipment()
            │   └─→ FastMCP Server (Shipping Service)
            └─→ MCP Tool: get_active_shipments()
                └─→ FastMCP Server (Shipping Service)
```

## Key Concepts

### 1. AgentTool Wraps Sub-Agent

```python
# Step 1: Create sub-agent with MCP tools
inventory_agent = LlmAgent(
    name="inventory_agent",
    tools=[inventory_mcp],  # MCPToolset
)

# Step 2: Wrap sub-agent as a tool
inventory_tool = AgentTool(agent=inventory_agent)

# Step 3: Main agent uses the wrapped agent as a tool
main_agent = LlmAgent(
    name="customer_service",
    tools=[inventory_tool],  # AgentTool, not the agent directly!
)
```

### 2. MCPToolset Points to FastMCP Server

```python
inventory_mcp = MCPToolset(
    name="inventory_mcp",
    server_command="python",
    server_args=["/path/to/mcp_server.py"],
)
```

When the sub-agent calls an MCP tool:
1. ADK starts the FastMCP server process
2. Communicates via MCP protocol
3. Gets the result
4. Returns to sub-agent
5. Sub-agent returns to main agent

### 3. Complete Lineage

When user asks: **"Is PROD-001 in stock?"**

```
invocation (total: 5234ms)
└─ agent_run [customer_service] (5230ms)
   ├─ call_llm (1200ms) ← Main agent decides to use inventory_agent
   │
   └─ execute_tool inventory_agent (3500ms) ⭐ AgentTool invocation
      │
      └─ invocation (3495ms) ← Sub-agent invocation starts
         │
         └─ agent_run [inventory_agent] (3490ms)
            │
            ├─ call_llm (800ms) ← Sub-agent decides to use check_stock
            │
            ├─ execute_tool check_stock (2100ms) ⭐ MCP Tool invocation
            │  └─ MCP Server call to Inventory Service
            │     └─ Returns: {"product_id": "PROD-001", "stock": 45}
            │
            └─ call_llm (590ms) ← Sub-agent formats response
   │
   └─ call_llm (530ms) ← Main agent formats final response
```

## What You See in ADK Web UI

### Trace Tab
- Complete nested structure
- Every tool call visible
- Timing for each step
- Clear parent-child relationships

### Events Tab
- Chronological event stream
- Tool calls and responses
- LLM calls and completions

### State Tab
- Session state (if any)
- Shared data between agents

## Comparison: Direct Tools vs AgentTool vs MCP

| Type | Example | Used By | Lineage |
|------|---------|---------|---------|
| **Direct Tool** | `get_store_hours()` | Main agent | `execute_tool get_store_hours` |
| **AgentTool** | `inventory_tool` | Main agent | `execute_tool inventory_agent` → `agent_run [inventory_agent]` |
| **MCP Tool** | `check_stock()` | Sub-agent | `execute_tool check_stock` → MCP server call |

## Why This Architecture?

### Benefits:
1. ✅ **Separation of Concerns** - Each agent has specific responsibility
2. ✅ **Reusability** - Sub-agents can be used by multiple main agents
3. ✅ **Scalability** - MCP servers can be deployed separately
4. ✅ **Observability** - Complete lineage visible in trace
5. ✅ **Flexibility** - Easy to add/remove capabilities

### When to Use Each Pattern:

**Direct Python Tool:**
- Simple, stateless operations
- No external dependencies
- Fast, synchronous operations
- Example: get_store_hours, calculate_discount

**AgentTool (Sub-Agent):**
- Complex decision-making needed
- Multiple related tools
- Specialized domain knowledge
- Example: inventory_agent, shipping_agent

**MCP Tool:**
- External service integration
- Database queries
- API calls
- Long-running operations
- Example: BigQuery, Looker, custom services

## Summary

### Your Questions Answered:

**Q: Where is MCP server tools used?**
A: MCP tools are used **inside sub-agents**, not directly by the main agent.

**Q: Is it used as a tool for the main agent?**
A: No! The **sub-agent** (wrapped as AgentTool) is the tool for the main agent. The MCP tool is used by the sub-agent.

**Q: How do I see lineage?**
A: In the Trace tab, you'll see:
- Main agent → AgentTool → Sub-agent → MCP Tool → Server

### The Pattern:

```
Main Agent
  uses → AgentTool (wrapped sub-agent)
           uses → MCPToolset
                    uses → FastMCP Server
```

This is the correct, production-ready pattern for multi-agent systems with MCP integration!

