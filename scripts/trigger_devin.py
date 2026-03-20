#!/usr/bin/env python3
"""
trigger_devin.py — called by GitHub Actions when API route files change.

Reads CHANGED_FILES from env, creates a Devin session referencing the
doc-sync playbook, and prints the session URL to the Actions log.
"""

import os
import sys
import requests

DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY", "")
DEVIN_ORG_ID = os.environ.get("DEVIN_ORG_ID", "")
DEVIN_PLAYBOOK_ID = os.environ.get("DEVIN_PLAYBOOK_ID", "")
CHANGED_FILES = os.environ.get("CHANGED_FILES", "")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")
GITHUB_SHA = os.environ.get("GITHUB_SHA", "")

BASE_URL = "https://api.devin.ai"


def main():
    for var, name in [
        (DEVIN_API_KEY, "DEVIN_API_KEY"),
        (DEVIN_ORG_ID, "DEVIN_ORG_ID"),
        (DEVIN_PLAYBOOK_ID, "DEVIN_PLAYBOOK_ID"),
    ]:
        if not var:
            print(f"ERROR: {name} environment variable is not set.", file=sys.stderr)
            sys.exit(1)

    if not CHANGED_FILES:
        print("No changed route files detected — skipping Devin trigger.")
        sys.exit(0)

    changed_list = [f.strip() for f in CHANGED_FILES.split(",") if f.strip()]
    print(f"Changed API files: {changed_list}")

    commit_ref = f"https://github.com/{GITHUB_REPOSITORY}/commit/{GITHUB_SHA}" if GITHUB_SHA else "unknown commit"

    message = (
        f"API route files have changed in commit {commit_ref}.\n\n"
        f"Changed files:\n"
        + "\n".join(f"  - {f}" for f in changed_list)
        + "\n\n"
        "Please update docs/api-reference.md to reflect the current state of all "
        "endpoints and open a draft PR titled 'docs: auto-update API reference'."
    )

    payload = {
        "prompt": message,
        "playbook_id": DEVIN_PLAYBOOK_ID,
    }

    headers = {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json",
    }

    url = f"{BASE_URL}/v3/organizations/{DEVIN_ORG_ID}/sessions"
    print(f"Creating Devin session at {url}...")

    response = requests.post(url, json=payload, headers=headers, timeout=30)

    if response.status_code not in (200, 201):
        print(
            f"ERROR: Devin API returned {response.status_code}: {response.text}",
            file=sys.stderr,
        )
        sys.exit(1)

    data = response.json()
    session_id = data.get("session_id") or data.get("id", "unknown")
    session_url = data.get("url") or f"https://app.devin.ai/sessions/{session_id}"

    print(f"Devin session created successfully.")
    print(f"  Session ID : {session_id}")
    print(f"  Session URL: {session_url}")
    print(f"\nDevin is now updating the API docs. Review the draft PR when it appears.")


if __name__ == "__main__":
    main()
