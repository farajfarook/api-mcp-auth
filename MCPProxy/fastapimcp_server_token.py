from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_mcp import AuthConfig, FastApiMCP

# Create FastAPI instance
app = FastAPI(title="Hello World API", version="1.0.0")

VALID_TOKEN = "secret123"  # Replace with your actual token

security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify the bearer token"""
    if credentials.credentials != VALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


@app.get("/", operation_id="read_root")
async def read_root():
    """Root endpoint that returns a hello world message"""
    return {"message": "Hello, World!"}


@app.get("/hello/{name}", operation_id="say_hello")
async def say_hello(name: str):
    """Personalized hello endpoint"""
    return {"message": f"Hello, {name}!"}


@app.get("/private", operation_id="private_endpoint")
async def private_endpoint(
    # Endpoint that requires token verification with valid token
    token=Depends(verify_token),
):
    """Private endpoint"""
    return {"message": "This is a private endpoint! called with token: " + token}


mcp = FastApiMCP(
    app,
    name="HelloWorldMCP",
    auth_config=AuthConfig(
        dependencies=[
            # Ensure token verification for all endpoints.
            # doesnt validate just check if the token is present
            Depends(security)
        ]
    ),
)
mcp.mount()

# Run the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
