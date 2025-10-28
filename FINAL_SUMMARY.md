

# Multi-Agent MCP Demo - Final Summary

This document summarizes the successful implementation and testing of a multi-agent system using Google ADK, demonstrating the agent-as-tool pattern with MCP integration.

## 1. Architecture

The system consists of a main customer service agent that utilizes two sub-agents as tools. These sub-agents, in turn, communicate with backend services via MCP (Model Context Protocol).

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

### Key Components:

*   **Main Agent (`customer_service`):** Handles initial user interaction and delegates tasks to the appropriate sub-agent or direct tool.
*   **Sub-Agents (`inventory_agent`, `shipping_agent`):** Specialized agents responsible for a single domain (inventory or shipping). They are wrapped as `AgentTool` for the main agent to use.
*   **MCP Servers (`inventory`, `shipping`):** Implemented using `FastMCP`, these servers provide the actual business logic for the tools used by the sub-agents.

## 2. Test Results

The system was tested using a series of queries to validate the functionality of direct tools, agent tools, and MCP integration. The tests were executed via the ADK CLI, and the results are captured below.

```
================================================================================
MULTI-AGENT MCP DEMO - TEST SUITE
================================================================================

================================================================================
TEST 1: Direct Tool - get_store_hours
================================================================================
Query: What are your store hours?

Running agent customer_service, type exit to exit.
/usr/local/lib/python3.11/dist-packages/google/adk/cli/cli.py:98: UserWarning: [EXPERIMENTAL] App: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  else App(name=session.app_name, root_agent=root_agent_or_app)
[user]: [customer_service]: Our store hours are:

*   Customer Service: 9 AM - 6 PM EST, Monday-Friday
*   Online Store: 24/7
*   Phone: 1-800-EXAMPLE
[user]: 
Aborted!

================================================================================
TEST 2: Direct Tool - get_return_policy
================================================================================
Query: What is your return policy?

Running agent customer_service, type exit to exit.
/usr/local/lib/python3.11/dist-packages/google/adk/cli/cli.py:98: UserWarning: [EXPERIMENTAL] App: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  else App(name=session.app_name, root_agent=root_agent_or_app)
[user]: [customer_service]: Our return policy allows for returns within 30 days of purchase. Items must be unopened and unused to be eligible for a return. Refunds will be issued to the original payment method. We do not charge a restocking fee for defective items. However, there is a 15% restocking fee for other returns.
[user]: 
Aborted!

================================================================================
TEST 3: Agent Tool - inventory_agent -> MCP check_stock
================================================================================
Query: Is PROD-001 in stock?

Running agent customer_service, type exit to exit.
/usr/local/lib/python3.11/dist-packages/google/adk/cli/cli.py:98: UserWarning: [EXPERIMENTAL] App: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  else App(name=session.app_name, root_agent=root_agent_or_app)
[user]: 

╭────────────────────────────────────────────────────────────────────────────╮
│                                                                            │
│        _ __ ___  _____           __  __  _____________    ____    ____     │
│       _ __ ___ .’____/___ ______/ /_/  |/  / ____/ __ \  |___ \  / __ \    │
│      _ __ ___ / /_  / __ `/ ___/ __/ /|_/ / /   / /_/ /  ___/ / / / / /    │
│     _ __ ___ / __/ / /_/ (__  ) /_/ /  / / /___/ ____/  /  __/_/ /_/ /     │
│    _ __ ___ /_/    \____/____/\__/_/  /_/\____/_/      /_____(*)____/      │
│                                                                            │
│                                                                            │
│                                FastMCP  2.0                                │
│                                                                            │
│                                                                            │
│                 🖥️  Server name:     Inventory Service                      │
│                 📦 Transport:       STDIO                                  │
│                                                                            │
│                 🏎️  FastMCP version: 2.12.4                                 │
--
[customer_service]: Yes, PROD-001 (Laptop Pro 15) is in stock.

[user]: 
Aborted!

================================================================================
TEST 4: Agent Tool - inventory_agent -> MCP get_low_stock_products
================================================================================
Query: Show me products with low stock

Running agent customer_service, type exit to exit.
/usr/local/lib/python3.11/dist-packages/google/adk/cli/cli.py:98: UserWarning: [EXPERIMENTAL] App: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  else App(name=session.app_name, root_agent=root_agent_or_app)
[user]: 

╭────────────────────────────────────────────────────────────────────────────╮
│                                                                            │
│        _ __ ___  _____           __  __  _____________    ____    ____     │
│       _ __ ___ .’____/___ ______/ /_/  |/  / ____/ __ \  |___ \  / __ \    │
│      _ __ ___ / /_  / __ `/ ___/ __/ /|_/ / /   / /_/ /  ___/ / / / / /    │
│     _ __ ___ / __/ / /_/ (__  ) /_/ /  / / /___/ ____/  /  __/_/ /_/ /     │
│    _ __ ___ /_/    \____/____/\__/_/  /_/\____/_/      /_____(*)____/      │
│                                                                            │
│                                                                            │
│                                FastMCP  2.0                                │
│                                                                            │
│                                                                            │
│                 🖥️  Server name:     Inventory Service                      │
│                 📦 Transport:       STDIO                                  │
│                                                                            │
│                 🏎️  FastMCP version: 2.12.4                                 │
--
[customer_service]: OK. The following product is low in stock: Monitor 27in (PROD-004), with 15 units remaining. Please consider restocking.

[user]: 
Aborted!

================================================================================
TEST 5: Agent Tool - shipping_agent -> MCP track_shipment
================================================================================
Query: Track shipment SHIP-002

Running agent customer_service, type exit to exit.
/usr/local/lib/python3.11/dist-packages/google/adk/cli/cli.py:98: UserWarning: [EXPERIMENTAL] App: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  else App(name=session.app_name, root_agent=root_agent_or_app)
[user]: 

╭────────────────────────────────────────────────────────────────────────────╮
│                                                                            │
│        _ __ ___  _____           __  __  _____________    ____    ____     │
│       _ __ ___ .’____/___ ______/ /_/  |/  / ____/ __ \  |___ \  / __ \    │
│      _ __ ___ / /_  / __ `/ ___/ __/ /|_/ / /   / /_/ /  ___/ / / / / /    │
│     _ __ ___ / __/ / /_/ (__  ) /_/ /  / / /___/ ____/  /  __/_/ /_/ /     │
│    _ __ ___ /_/    \____/____/\__/_/  /_/\____/_/      /_____(*)____/      │
│                                                                            │
│                                                                            │
│                                FastMCP  2.0                                │
│                                                                            │
│                                                                            │
│                 🖥️  Server name:     Shipping Service                       │
│                 📦 Transport:       STDIO                                  │
│                                                                            │
│                 🏎️  FastMCP version: 2.12.4                                 │
--
[customer_service]: Shipment SHIP-002 is currently In Transit. It was last seen in Chicago.

[user]: 
Aborted!

================================================================================
TEST 6: Agent Tool - shipping_agent -> MCP get_active_shipments
================================================================================
Query: Show me all active shipments

Running agent customer_service, type exit to exit.
/usr/local/lib/python3.11/dist-packages/google/adk/cli/cli.py:98: UserWarning: [EXPERIMENTAL] App: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  else App(name=session.app_name, root_agent=root_agent_or_app)
[user]: [customer_service]: There are 2 active shipments:

*   SHIP-002: In Transit
*   SHIP-003: Processing
[user]: 
Aborted!

================================================================================
ALL TESTS COMPLETED
================================================================================

Architecture Demonstrated:
  Main Agent (customer_service)
  ├─→ Direct Tools: get_store_hours(), get_return_policy()
  ├─→ AgentTool: inventory_agent
  │   └─→ MCPToolset: Inventory MCP Server (FastMCP)
  │       ├─→ check_stock()
  │       └─→ get_low_stock_products()
  └─→ AgentTool: shipping_agent
      └─→ MCPToolset: Shipping MCP Server (FastMCP)
          ├─→ track_shipment()
          └─→ get_active_shipments()

✅ Main agent uses sub-agents as tools (AgentTool pattern)
✅ Sub-agents use MCP tools (MCPToolset pattern)
✅ FastMCP servers provide the actual tool implementations
✅ Complete lineage tracking available in ADK web UI Trace tab


## 3. Key Takeaways & Observations

*   **Agent-as-Tool Pattern:** The main agent successfully uses sub-agents as tools, demonstrating a clean and modular approach to building complex agentic systems.
*   **MCP Integration:** Sub-agents seamlessly integrate with backend services via MCP, abstracting the tool implementation details from the agent logic.
*   **Lineage and Traceability:** While the web UI had some rendering issues, the ADK CLI provides a reliable way to test agent functionality. The full lineage of agent and tool calls is available in the ADK web UI's "Trace" tab, providing excellent visibility into the system's execution flow.
*   **ADK API Changes:** The project was updated to reflect recent changes in the `google-adk` library, specifically the `MCPToolset` and `Session` APIs.

## 4. How to Run the Demo

1.  **Unzip the project archive.**
2.  **Install dependencies:**

    ```bash
    pip install google-adk fastmcp
    ```

3.  **Set your Google API Key:**

    ```bash
    export GOOGLE_API_KEY="your-api-key"
    ```

4.  **Run the ADK Web UI:**

    ```bash
    cd adk-simple-mcp-demo
    adk web --host 0.0.0.0 --port 8004 agents
    ```

5.  **Access the Web UI:**

    Open your browser to `http://0.0.0.0:8004`.

6.  **Run the CLI tests:**

    ```bash
    ./run_tests.sh
    ```

