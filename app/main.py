import json
import os
import sys
from datetime import datetime, timezone

import requests


def main() -> int:
    target_url = os.environ.get("TARGET_URL", "").strip()
    if not target_url:
        print("ERROR: TARGET_URL is not set. Add it as a GitHub Secret named TARGET_URL.", file=sys.stderr)
        return 2

    auth_token = os.environ.get("AUTH_TOKEN", "").strip()

    # Example JSON payload (customize as you like)
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
        resp = requests.post(
            target_url,
            data=json.dumps(payload),
            headers=headers,
            timeout=30,
        )

        print(f"POST {target_url}")
        print(f"Status: {resp.status_code}")

        # Print headers (optional; comment out if noisy)
        # print("Response headers:", dict(resp.headers))

        # Print body safely
        content_type = (resp.headers.get("Content-Type") or "").lower()
        print("----- Response body (first 20k chars) -----")
        if "application/json" in content_type:
            try:
                print(json.dumps(resp.json(), ensure_ascii=False, indent=2)[:20000])
            except Exception:
                print(resp.text[:20000])
        else:
            print(resp.text[:20000])

        # Fail the workflow on HTTP 4xx/5xx if you want:
        # resp.raise_for_status()

        return 0

    except requests.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
