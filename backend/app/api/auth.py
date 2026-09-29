"""Authentication gate for every request the backend serves.

AUTH_MODE controls how callers are authenticated:

- "easyauth": Azure Container Apps built-in authentication (EasyAuth) is
  enabled in front of the app. Requests must carry the
  X-MS-CLIENT-PRINCIPAL-ID header, which the platform sets for signed-in
  callers and strips from any client-supplied request.
- "anonymous": no authentication. Only use this for local development or
  when another trusted gateway authenticates every request.

When AUTH_MODE is unset or has any other value, every request is rejected.
"""

import json
import logging
import os
from typing import Mapping

logger = logging.getLogger("uvicorn")

PRINCIPAL_ID_HEADER = b"x-ms-client-principal-id"

_UNAUTHORIZED_BODY = json.dumps({"detail": "Unauthorized"}).encode()


def resolve_auth_mode(env: Mapping[str, str] = os.environ) -> str:
    mode = (env.get("AUTH_MODE") or "").strip().lower()
    if mode in ("easyauth", "anonymous"):
        return mode
    return "unconfigured"


def _has_principal(scope) -> bool:
    for name, value in scope.get("headers", []):
        if name.lower() == PRINCIPAL_ID_HEADER and value.strip():
            return True
    return False


class AuthMiddleware:
    """ASGI middleware that runs before routing, so it also covers static
    file mounts and the generated API docs."""

    def __init__(self, app):
        self.app = app
        self._warned = False

    def _warn_once(self, message: str):
        if not self._warned:
            self._warned = True
            logger.warning(f"[auth] {message}")

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        mode = resolve_auth_mode()

        if mode == "anonymous":
            self._warn_once(
                "AUTH_MODE=anonymous: the API is reachable without authentication."
            )
            await self.app(scope, receive, send)
            return

        if mode == "easyauth" and _has_principal(scope):
            await self.app(scope, receive, send)
            return

        if mode == "unconfigured":
            self._warn_once(
                "Rejecting requests because authentication is not configured. "
                "Enable Azure Container Apps authentication and set AUTH_MODE=easyauth, "
                "or set AUTH_MODE=anonymous for local development."
            )

        if scope["type"] == "websocket":
            await send({"type": "websocket.close", "code": 1008})
            return

        await send(
            {
                "type": "http.response.start",
                "status": 401,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", str(len(_UNAUTHORIZED_BODY)).encode()),
                    (b"cache-control", b"no-store"),
                ],
            }
        )
        await send({"type": "http.response.body", "body": _UNAUTHORIZED_BODY})
