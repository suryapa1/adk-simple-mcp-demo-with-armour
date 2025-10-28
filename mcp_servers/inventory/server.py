"""Simple Inventory FastMCP Server"""
from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Inventory Service")

# Simple in-memory inventory data
INVENTORY = {
    "PROD-001": {"name": "Laptop Pro 15", "stock": 45, "price": 1299.99},
    "PROD-002": {"name": "Wireless Mouse", "stock": 120, "price": 29.99},
    "PROD-003": {"name": "USB-C Cable", "stock": 200, "price": 12.99},
    "PROD-004": {"name": "Monitor 27in", "stock": 15, "price": 399.99},
}

@mcp.tool()
def check_stock(product_id: str) -> dict:
    """Check stock level for a product
    
    Args:
        product_id: Product ID (e.g., PROD-001)
    
    Returns:
        Product details with stock level
    """
    if product_id in INVENTORY:
        return {
            "product_id": product_id,
            **INVENTORY[product_id],
            "in_stock": INVENTORY[product_id]["stock"] > 0
        }
    return {"error": f"Product {product_id} not found"}

@mcp.tool()
def get_low_stock_products(threshold: int = 20) -> dict:
    """Get products with stock below threshold
    
    Args:
        threshold: Stock level threshold (default: 20)
    
    Returns:
        List of low stock products
    """
    low_stock = [
        {"product_id": pid, **data}
        for pid, data in INVENTORY.items()
        if data["stock"] < threshold
    ]
    return {
        "threshold": threshold,
        "count": len(low_stock),
        "products": low_stock
    }

if __name__ == "__main__":
    # Run MCP server
    mcp.run()

