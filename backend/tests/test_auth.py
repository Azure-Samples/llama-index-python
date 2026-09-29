import os
import tempfile
import unittest
from unittest import mock

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient

from app.api.auth import AuthMiddleware, resolve_auth_mode

PRINCIPAL = {"X-MS-CLIENT-PRINCIPAL-ID": "00000000-0000-0000-0000-000000000001"}


def build_client(static_dir: str) -> TestClient:
    app = FastAPI()
    app.add_middleware(AuthMiddleware)

    @app.post("/api/chat")
    async def chat():
        return {"ok": True}

    @app.get("/api/chat/config")
    async def config():
        return {"ok": True}

    app.mount("/api/files/data", StaticFiles(directory=static_dir))
    return TestClient(app)


class ResolveAuthModeTest(unittest.TestCase):
    def test_modes(self):
        self.assertEqual(resolve_auth_mode({}), "unconfigured")
        self.assertEqual(resolve_auth_mode({"AUTH_MODE": ""}), "unconfigured")
        self.assertEqual(resolve_auth_mode({"AUTH_MODE": "bogus"}), "unconfigured")
        self.assertEqual(resolve_auth_mode({"AUTH_MODE": " EasyAuth "}), "easyauth")
        self.assertEqual(resolve_auth_mode({"AUTH_MODE": "anonymous"}), "anonymous")


class AuthMiddlewareTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        with open(os.path.join(self.tmp.name, "doc.txt"), "w") as f:
            f.write("hello")
        self.client = build_client(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def requests(self, headers=None):
        return [
            self.client.post("/api/chat", json={}, headers=headers),
            self.client.get("/api/chat/config", headers=headers),
            self.client.get("/api/files/data/doc.txt", headers=headers),
            self.client.get("/docs", headers=headers),
        ]

    def assert_all(self, responses, status):
        for response in responses:
            self.assertEqual(response.status_code, status, response.request.url)

    def assert_rejected(self, responses):
        self.assert_all(responses, 401)
        for response in responses:
            self.assertEqual(response.headers["cache-control"], "no-store")
            self.assertEqual(response.json(), {"detail": "Unauthorized"})

    def test_unset_rejects_everything(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assert_rejected(self.requests())
            self.assert_rejected(self.requests(PRINCIPAL))

    def test_unknown_value_rejects_everything(self):
        with mock.patch.dict(os.environ, {"AUTH_MODE": "disabled"}, clear=True):
            self.assert_rejected(self.requests(PRINCIPAL))

    def test_easyauth_requires_principal(self):
        with mock.patch.dict(os.environ, {"AUTH_MODE": "easyauth"}, clear=True):
            self.assert_rejected(self.requests())
            self.assert_rejected(self.requests({"X-MS-CLIENT-PRINCIPAL-ID": " "}))
            self.assert_all(self.requests(PRINCIPAL), 200)
            self.assertEqual(
                self.client.get("/api/files/data/doc.txt", headers=PRINCIPAL).text,
                "hello",
            )

    def test_anonymous_allows_everything(self):
        with mock.patch.dict(os.environ, {"AUTH_MODE": "anonymous"}, clear=True):
            self.assert_all(self.requests(), 200)


if __name__ == "__main__":
    unittest.main()
