"""Simple Shipping FastMCP Server"""
from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Shipping Service")

# Simple in-memory shipping data
SHIPMENTS = {
    "SHIP-001": {"order_id": "ORD-2024-001", "status": "delivered", "location": "Customer Address"},
    "SHIP-002": {"order_id": "ORD-2024-002", "status": "in_transit", "location": "Distribution Center - Chicago"},
    "SHIP-003": {"order_id": "ORD-2024-003", "status": "processing", "location": "Warehouse - Seattle"},
}

@mcp.tool()
def track_shipment(tracking_number: str) -> dict:
    """Track a shipment by tracking number
    
    Args:
        tracking_number: Shipment tracking number (e.g., SHIP-001)
    
    Returns:
        Shipment status and location
    """
    if tracking_number in SHIPMENTS:
        return {
            "tracking_number": tracking_number,
            **SHIPMENTS[tracking_number]
        }
    return {"error": f"Tracking number {tracking_number} not found"}

@mcp.tool()
def get_active_shipments() -> dict:
    """Get all active (non-delivered) shipments
    
    Returns:
        List of active shipments
    """
    active = [
        {"tracking_number": tid, **data}
        for tid, data in SHIPMENTS.items()
        if data["status"] != "delivered"
    ]
    return {
        "count": len(active),
        "shipments": active
    }

if __name__ == "__main__":
    # Run MCP server
    mcp.run()

