# Chapter 10. Function Calling – example 7 (manuscript: 10-funktsii.md, line 314)
# smereka_mcp/server.py – MCP server of Smereka's tracking system
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations
from trembita import tools

server = MCPServer("smereka-tracking",
                   instructions="Shipment tracking and warehouses of the Smereka company.")

@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def track_shipment(shipment_id: str) -> dict:
    """Status and location of a shipment by a number like SM-2610-0042."""
    return tools.track_shipment(shipment_id)

@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def find_warehouse(city: str) -> dict:
    """Address, opening hours and phone number of Smereka's warehouse in a city."""
    return tools.find_warehouse(city)

if __name__ == "__main__":
    server.run()                       # stdio transport by default
