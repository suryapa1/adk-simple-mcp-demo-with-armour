#!/bin/bash
# Test script for multi-agent MCP demo

export GOOGLE_API_KEY=
cd /home/ubuntu/adk-simple-mcp-demo

echo "================================================================================"
echo "MULTI-AGENT MCP DEMO - TEST SUITE"
echo "================================================================================"
echo ""

# Test 1: Direct tool - store hours
echo "================================================================================"
echo "TEST 1: Direct Tool - get_store_hours"
echo "================================================================================"
echo "Query: What are your store hours?"
echo ""
echo "What are your store hours?" | timeout 30 adk run agents/main_agent 2>&1 | grep -A 20 "customer_service"
echo ""

# Test 2: Direct tool - return policy
echo "================================================================================"
echo "TEST 2: Direct Tool - get_return_policy"
echo "================================================================================"
echo "Query: What is your return policy?"
echo ""
echo "What is your return policy?" | timeout 30 adk run agents/main_agent 2>&1 | grep -A 20 "customer_service"
echo ""

# Test 3: Inventory agent - check stock
echo "================================================================================"
echo "TEST 3: Agent Tool - inventory_agent -> MCP check_stock"
echo "================================================================================"
echo "Query: Is PROD-001 in stock?"
echo ""
echo "Is PROD-001 in stock?" | timeout 30 adk run agents/main_agent 2>&1 | grep -A 20 "customer_service"
echo ""

# Test 4: Inventory agent - low stock
echo "================================================================================"
echo "TEST 4: Agent Tool - inventory_agent -> MCP get_low_stock_products"
echo "================================================================================"
echo "Query: Show me products with low stock"
echo ""
echo "Show me products with low stock" | timeout 30 adk run agents/main_agent 2>&1 | grep -A 20 "customer_service"
echo ""

# Test 5: Shipping agent - track shipment
echo "================================================================================"
echo "TEST 5: Agent Tool - shipping_agent -> MCP track_shipment"
echo "================================================================================"
echo "Query: Track shipment SHIP-002"
echo ""
echo "Track shipment SHIP-002" | timeout 30 adk run agents/main_agent 2>&1 | grep -A 20 "customer_service"
echo ""

# Test 6: Shipping agent - active shipments
echo "================================================================================"
echo "TEST 6: Agent Tool - shipping_agent -> MCP get_active_shipments"
echo "================================================================================"
echo "Query: Show me all active shipments"
echo ""
echo "Show me all active shipments" | timeout 30 adk run agents/main_agent 2>&1 | grep -A 20 "customer_service"
echo ""

echo "================================================================================"
echo "ALL TESTS COMPLETED"
echo "================================================================================"
echo ""
echo "Architecture Demonstrated:"
echo "  Main Agent (customer_service)"
echo "  ├─→ Direct Tools: get_store_hours(), get_return_policy()"
echo "  ├─→ AgentTool: inventory_agent"
echo "  │   └─→ MCPToolset: Inventory MCP Server (FastMCP)"
echo "  │       ├─→ check_stock()"
echo "  │       └─→ get_low_stock_products()"
echo "  └─→ AgentTool: shipping_agent"
echo "      └─→ MCPToolset: Shipping MCP Server (FastMCP)"
echo "          ├─→ track_shipment()"
echo "          └─→ get_active_shipments()"
echo ""
echo "✅ Main agent uses sub-agents as tools (AgentTool pattern)"
echo "✅ Sub-agents use MCP tools (MCPToolset pattern)"
echo "✅ FastMCP servers provide the actual tool implementations"
echo "✅ Complete lineage tracking available in ADK web UI Trace tab"

