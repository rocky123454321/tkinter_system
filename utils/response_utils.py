"""Standard response helpers for controllers."""

from __future__ import annotations

from typing import Any


def ok(data: Any | None = None) -> dict[str, Any]:
    """Build an OK response dict."""

    return {"ok": True, "data": data}


def error(message: str, *, code: str | None = None) -> dict[str, Any]:
    """Build an error response dict."""

    payload: dict[str, Any] = {"ok": False, "error": message}
    if code is not None:
        payload["code"] = code
    return payload

