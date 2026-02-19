import json
import os
import sys
from datetime import datetime, timezone

import requests


DEFAULT_URL = "https://httpbin.org/post"


def main() -> int:
    target_url = os.environ.get("TARGET_URL", "").strip()

    if not target_url:
        print("No TARGET_URL provided. Using default:", DEFAULT_URL)
        target_url = DEFAULT_URL

    auth_token = os.environ.get("AUTH_TOKEN", "").strip()

    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event": "hourly_ping",
        "source": "github-actions",
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "hourly-post-bot/1.0",
    }

    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    try:
        response = requests.post(
            target_url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        print(f"\nPOST to: {target_url}")
        print("Status code:", response.status_code)
        print("----- Response body -----")
        print(response.text[:20000])  # limit to 20k chars

        return 0

    except requests.RequestException as e:
        print("Request failed:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
