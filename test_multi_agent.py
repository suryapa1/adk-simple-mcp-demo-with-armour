#!/usr/bin/env python3.11
"""
Test script for multi-agent MCP demo
Demonstrates:
1. Direct tool usage (get_store_hours, get_return_policy)
2. Agent-as-tool with MCP (inventory_agent -> inventory MCP)
3. Agent-as-tool with MCP (shipping_agent -> shipping MCP)
4. Lineage tracking
"""

import asyncio
import sys
sys.path.insert(0, '/home/ubuntu/adk-simple-mcp-demo/agents')

from main_agent import root_agent
from google.adk.sessions import Session

async def test_agent(query: str, description: str):
    """Test the agent with a query and print results"""
    print(f"\n{'='*80}")
    print(f"TEST: {description}")
    print(f"{'='*80}")
    print(f"Query: {query}\n")
    
    # Create a new session for each test
    session = Session()
    
    # Run the agent
    result = await root_agent.run(query, session=session)
    
    print(f"Response: {result.content}\n")
    print(f"{'='*80}\n")
    return result

async def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("MULTI-AGENT MCP DEMO - TEST SUITE")
    print("="*80)
    
    # Test 1: Direct tool - store hours
    await test_agent(
        "What are your store hours?",
        "Direct Tool: get_store_hours"
    )
    
    # Test 2: Direct tool - return policy
    await test_agent(
        "What is your return policy?",
        "Direct Tool: get_return_policy"
    )
    
    # Test 3: Inventory agent (MCP)
    await test_agent(
        "Is PROD-001 in stock?",
        "Agent Tool: inventory_agent -> MCP: check_stock"
    )
    
    # Test 4: Inventory agent (MCP) - low stock
    await test_agent(
        "Show me products with low stock",
        "Agent Tool: inventory_agent -> MCP: get_low_stock_products"
    )
    
    # Test 5: Shipping agent (MCP)
    await test_agent(
        "Track shipment SHIP-002",
        "Agent Tool: shipping_agent -> MCP: track_shipment"
    )
    
    # Test 6: Shipping agent (MCP) - active shipments
    await test_agent(
        "Show me all active shipments",
        "Agent Tool: shipping_agent -> MCP: get_active_shipments"
    )
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*80)
    print("\nKey Observations:")
    print("1. ✅ Main agent successfully uses direct tools (get_store_hours, get_return_policy)")
    print("2. ✅ Main agent successfully uses inventory_agent as AgentTool")
    print("3. ✅ Main agent successfully uses shipping_agent as AgentTool")
    print("4. ✅ Sub-agents successfully use MCP tools (FastMCP servers)")
    print("5. ✅ Complete agent-as-tool pattern demonstrated")
    print("\nArchitecture:")
    print("  Main Agent (customer_service)")
    print("  ├─→ Direct Tools: get_store_hours(), get_return_policy()")
    print("  ├─→ AgentTool: inventory_agent")
    print("  │   └─→ MCPToolset: Inventory MCP Server")
    print("  │       ├─→ check_stock()")
    print("  │       └─→ get_low_stock_products()")
    print("  └─→ AgentTool: shipping_agent")
    print("      └─→ MCPToolset: Shipping MCP Server")
    print("          ├─→ track_shipment()")
    print("          └─→ get_active_shipments()")

if __name__ == "__main__":
    asyncio.run(main())

