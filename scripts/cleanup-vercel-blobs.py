#!/usr/bin/env python3
"""Remove unlinked duplicate Vercel Blob stores for this project."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

KEEP_STORES = {"store_VRKRybkmfOo12ivC"}
REMOVE_NAMES = {
    "80s-jazzercise-party",
    "80s-jazzercise-blob-final",
}


def load_token() -> str:
    auth_path = Path(os.environ["APPDATA"]) / "com.vercel.cli" / "Data" / "auth.json"
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    return data["token"]


def api(method: str, path: str, token: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        f"https://api.vercel.com{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    token = load_token()
    team_id = "team_CAcqm20HCv68FPpjwpyKEJou"
    stores = api("GET", f"/v1/blob/stores?teamId={team_id}", token).get("stores", [])

    removed = 0
    for store in stores:
        store_id = store.get("id", "")
        name = store.get("name", "")
        if store_id in KEEP_STORES or name not in REMOVE_NAMES:
            print(f"keep  {name} ({store_id})")
            continue
        try:
            api("DELETE", f"/v1/blob/stores/{store_id}?teamId={team_id}", token)
            print(f"removed {name} ({store_id})")
            removed += 1
        except urllib.error.HTTPError as exc:
            print(f"failed  {name} ({store_id}) — {exc.code}")

    print(f"\nRemoved {removed} orphan store(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
