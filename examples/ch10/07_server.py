# Розділ 10. Виклик функцій – приклад 7 (рукопис: 10-funktsii.md, рядок 314)
# smereka_mcp/server.py – MCP-сервер системи відстеження «Смереки»
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations
from trembita import tools

server = MCPServer("smereka-tracking",
                   instructions="Відстеження відправлень і склади компанії «Смерека».")

@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def track_shipment(shipment_id: str) -> dict:
    """Статус і місцезнаходження відправлення за номером виду SM-2610-0042."""
    return tools.track_shipment(shipment_id)

@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def find_warehouse(city: str) -> dict:
    """Адреса, графік роботи й телефон складу «Смереки» в місті."""
    return tools.find_warehouse(city)

if __name__ == "__main__":
    server.run()                       # транспорт stdio за замовчуванням
