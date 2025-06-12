from fastapi.testclient import TestClient
import main

class MockResponse:
    def __init__(self, content=b'{"hello": "world"}', status_code=200, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {"content-type": "application/json"}

class MockAsyncClient:
    def __init__(self, *args, **kwargs):
        pass
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        pass
    async def get(self, url, *args, **kwargs):
        return MockResponse()
    async def request(self, method, url, params=None, content=None, headers=None):
        return MockResponse()

def test_proxy(monkeypatch):
    monkeypatch.setattr(main.httpx, "AsyncClient", MockAsyncClient)
    client = TestClient(main.app)
    resp = client.get("/some/path")
    assert resp.status_code == 200
    assert resp.json() == {"hello": "world"}
