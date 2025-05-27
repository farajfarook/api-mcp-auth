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
    "client_id": "mcpclient",
    "client_secret": "mcpclient_secret",
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
            return claims

    except Exception as e:
        logger.error(f"Auth error: {str(e)}")
        logger.error(f"Request URL: {request.url}")
        logger.error(f"Request headers: {dict(request.headers)}")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


async def get_current_user_id(claims: dict = Depends(verify_auth)) -> str:
    user_id = claims.get("sub")

    if not user_id:
        logger.error("No user ID found in token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return user_id


@app.get("/api/public", operation_id="public")
async def public():
    return {"message": "This is a public route"}


@app.get("/api/protected", operation_id="protected")
async def protected(user_id: str = Depends(get_current_user_id)):
    return {"message": f"Hello, {user_id}!", "user_id": user_id}


mcp = FastApiMCP(
    app,
    name="MCP With OAuth",
    auth_config=AuthConfig(
        issuer=settings["issuer"],
        authorize_url=f"{issuer_url}/connect/authorize",
        oauth_metadata_url=f"{issuer_url}/.well-known/openid-configuration",
        audience=settings["audience"],
        client_id=settings["client_id"],
        client_secret=settings["client_secret"],
        default_scope="openid profile email",
        dependencies=[Depends(verify_auth)],
        setup_proxies=True,
    ),
)

mcp.mount()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8009)
