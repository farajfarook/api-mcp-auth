from mcp.server.fastmcp import FastMCP

mcp = FastMCP()


@mcp.tool()
def get_weather() -> str:
    """
    Get the current weather.
    """
    return "Sunny, 25°C"
