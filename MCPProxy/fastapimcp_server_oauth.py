import logging
import os
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi_mcp import FastApiMCP, AuthConfig

from shared.auth import fetch_jwks_public_key
from shared.setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

settings = {
    "issuer": "http://localhost:5001",
    "audience": "http://localhost:5001/resources",
    "client_id": "interactive",
    "client_secret": "interactive_secret",
    "scope": "openid profile email api weatherget",
}

issuer_url = os.getenv("ISSUER_URL", settings["issuer"])


async def lifespan(app: FastAPI):
    app.state.jwks_public_key = await fetch_jwks_public_key(
        f"{issuer_url}/.well-known/openid-configuration/jwks"
    )
    yield


app = FastAPI(lifespan=lifespan)


async def verify_auth(request: Request) -> dict[str, Any]:
    import jwt

    try:
        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header",
            )

        token = auth_header.split(" ")[1]

        header = jwt.get_unverified_header(token)

        # Check if this is a JWE token (encrypted token)
        if header.get("alg") == "dir" and header.get("enc") == "A256GCM":
            raise ValueError(
                "Token is encrypted, offline validation not possible. "
                "This is usually due to not specifying the audience when requesting the token."
            )

        # Otherwise, it's a JWT, we can validate it offline
        if header.get("alg") in ["RS256", "HS256"]:
            claims = jwt.decode(
                token,
                app.state.jwks_public_key,
                algorithms=["RS256", "HS256"],
                audience=settings["audience"],
                issuer=settings["issuer"],
                options={"verify_signature": True},
            )
            return {"token": token, "claims": claims}

    except Exception as e:
        logger.error(f"Auth error: {str(e)}")
        logger.error(f"Request URL: {request.url}")
        logger.error(f"Request headers: {dict(request.headers)}")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


async def get_token(auth_data: dict = Depends(verify_auth)) -> str:
    token = auth_data.get("token")

    if not token:
        logger.error("No token found in auth data")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return token


async def get_claims(auth_data: dict = Depends(verify_auth)) -> dict:
    claims = auth_data.get("claims", {})

    if not claims:
        logger.error("No claims found in auth data")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return claims


async def get_current_user_id(claims: dict = Depends(get_claims)) -> str:
    user_id = claims.get("sub")

    if not user_id:
        logger.error("No user ID found in token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return user_id


async def get_scope(claims: dict = Depends(get_claims)) -> str:
    scope = claims.get("scope")

    if not scope:
        logger.error("No scope found in token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return scope


@app.get("/api/public", operation_id="public")
async def public():
    return {"message": "This is a public route"}


@app.get("/api/protected", operation_id="protected")
async def protected(
    user_id: str = Depends(get_current_user_id), scope: str = Depends(get_scope)
):
    return {"message": f"Hello, {user_id}!", "user_id": user_id, "scope": scope}


@app.get("/api/get_weather", operation_id="get_weather")
async def get_weather(token: str = Depends(get_token)):
    """
    This endpoint is protected and requires the 'weatherget' scope.
    """
    return {"message": "Weather data"}


mcp = FastApiMCP(
    app,
    name="MCP With OAuth",
    auth_config=AuthConfig(
        issuer=settings["issuer"],
        authorize_url=f"{settings['issuer']}/connect/authorize",
        oauth_metadata_url=f"{settings['issuer']}/.well-known/openid-configuration",
        audience=settings["audience"],
        client_id=settings["client_id"],
        client_secret=settings["client_secret"],
        default_scope=settings["scope"],
        dependencies=[Depends(verify_auth)],
        setup_proxies=True,
    ),
)

mcp.mount()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8010)
