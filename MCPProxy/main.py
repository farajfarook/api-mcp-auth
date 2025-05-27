from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings

mcp = FastMCP(
    name="WeatherService",
    auth_server_provider="http://localhost:5001",
    auth=AuthSettings(
        issuer_url="http://localhost:5001",
        client_id="interactive",
        required_scopes=("openid", "profile", "api", "weatherget"),
        post_logout_redirect_uri="http://localhost:5173/signout-callback-oidc",
        redirect_uri="http://localhost:5173/signin-oidc",
        response_type="code",
    ),
)


@mcp.tool()
def get_weather() -> str:
    """
    Get the current weather.
    """
    return "Sunny, 25°C"


if __name__ == "__main__":
    mcp.run("sse")
