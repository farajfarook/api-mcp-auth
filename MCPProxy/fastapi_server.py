from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from fastapi_mcp import AuthConfig, FastApiMCP

# Create FastAPI instance
app = FastAPI(title="Hello World API", version="1.0.0")

token_auth_scheme = HTTPBearer()


@app.get("/", operation_id="read_root")
async def read_root():
    """Root endpoint that returns a hello world message"""
    return {"message": "Hello, World!"}


@app.get("/hello/{name}", operation_id="say_hello")
async def say_hello(name: str):
    """Personalized hello endpoint"""
    return {"message": f"Hello, {name}!"}


@app.get("/private", operation_id="private_endpoint")
async def private_endpoint(token=Depends(token_auth_scheme)):
    """Private endpoint"""
    return {"message": "This is a private endpoint!"}


mcp = FastApiMCP(
    app,
    name="HelloWorldMCP",
)
mcp.mount()

# Run the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
