import httpx
from fastapi import FastAPI, Request, Response

SPEC_URL = "https://api.eu.cast.ai/v1/spec/preview/openapi.json"
API_BASE = "https://api.eu.cast.ai"

app = FastAPI(title="CastAI MCP Proxy")

@app.get("/openapi.json")
async def get_spec():
    async with httpx.AsyncClient() as client:
        resp = await client.get(SPEC_URL)
    return Response(content=resp.content, media_type="application/json")

async def proxy(request: Request, full_path: str):
    method = request.method
    headers = dict(request.headers)
    headers.pop("host", None)
    params = dict(request.query_params)
    body = await request.body()

    async with httpx.AsyncClient(base_url=API_BASE) as client:
        resp = await client.request(method, f"/{full_path}", params=params, content=body, headers=headers)
    return Response(content=resp.content, status_code=resp.status_code, headers={"content-type": resp.headers.get("content-type", "application/json")})

# Capture all paths
for method in ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]:
    app.add_api_route("/{full_path:path}", proxy, methods=[method])
