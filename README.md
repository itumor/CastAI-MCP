# CastAI MCP Proxy Server

This repository contains a small FastAPI server that proxies requests to the [CAST AI API](https://api.eu.cast.ai). The server exposes the same OpenAPI schema available at `https://api.eu.cast.ai/v1/spec/preview/openapi.json` and forwards all incoming requests to the remote API.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn main:app --reload
```

You can then send requests to `http://localhost:8000/...` and they will be proxied to `https://api.eu.cast.ai/...`.
