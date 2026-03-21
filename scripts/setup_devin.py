#!/usr/bin/env python3
"""
setup_devin.py — one-time setup script, run locally before first use.

Creates:
  1. A reusable playbook for doc-sync sessions
  2. A knowledge note with DataStack's doc conventions

Prints the IDs you need to add as GitHub secrets:
  DEVIN_PLAYBOOK_ID

Usage:
  export DEVIN_API_KEY=your_key
  export DEVIN_ORG_ID=your_org_id
  python scripts/setup_devin.py
"""

import os
import sys
import json
import requests

DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY", "")
DEVIN_ORG_ID = os.environ.get("DEVIN_ORG_ID", "")
BASE_URL = "https://api.devin.ai"

PLAYBOOK_NAME = "DataStack API Doc Sync"
PLAYBOOK_CONTENT = """\
You are DataStack's documentation engineer. When triggered with a list of changed API route files:

1. Clone or access the repository. Read each changed file in full to understand what endpoints exist,
   their HTTP methods, URL paths, request bodies, response schemas, and authentication requirements.

2. Read the current docs/api-reference.md to understand what is already documented.

3. Update docs/api-reference.md to accurately reflect ALL current endpoints. For each endpoint document:
   - One-line description of what the endpoint does
   - Authentication: the Authorization header format (Bearer token)
   - Request parameters: path params, query params, and request body fields with types and whether required
   - Response schema: all fields with types, and the HTTP status code
   - A working curl example

4. Do NOT modify the Architecture or Concepts sections — only the API Reference section.

5. Open a draft PR titled "docs: auto-update API reference" with a description that includes:
   - A summary table of what changed (endpoint | change type | one-line summary)
   - A link to the commit that triggered this update
   - Note that this PR was generated automatically by Devin

Be accurate. If a field is documented with the wrong type or name in the existing docs, correct it.
If an endpoint exists in code but not in docs, add it. If an endpoint was removed from code, remove it from docs.
"""

KNOWLEDGE_NOTE_NAME = "DataStack API Doc Conventions"
KNOWLEDGE_NOTE_CONTENT = """\
DataStack API Documentation Conventions:

FORMAT:
- Use Markdown (not YAML/OpenAPI spec)
- Organize by resource (Users, Products, Orders, etc.)
- Each endpoint gets its own ### heading with the HTTP method and path

REQUIRED SECTIONS FOR EACH ENDPOINT:
1. Description — one sentence explaining what the endpoint does and any important behavior
2. Authentication — always document the Authorization header: `Authorization: Bearer <token>`
3. Request — document path parameters, query parameters, and request body fields
   - Use a table: | Field | Type | Required | Description |
   - For request body, also include a JSON example block
4. Response — document all response fields with types and the success HTTP status code
   - Include a JSON example block showing a realistic response
5. Curl example — a complete, copy-pasteable curl command

STYLE:
- Tone: concise and technical, no marketing language
- Use backticks for field names, types, and values
- Prices/amounts: always clarify units (e.g., `price_cents` — integer, USD cents)
- Status enums: list all valid values

DRAFT PRs:
- Title: "docs: auto-update API reference"
- PR description must include:
  - Summary table: | Endpoint | Change | Summary |
  - Link to the triggering commit
  - "Generated automatically by Devin"
- Open as draft so a human reviews before merge

AUTH PATTERN:
- All endpoints use Bearer token auth via the Authorization header
- NOT query parameter API keys (the old pattern was deprecated)
"""


def create_playbook(headers: dict) -> str:
    url = f"{BASE_URL}/v3/organizations/{DEVIN_ORG_ID}/playbooks"
    payload = {
        "title": PLAYBOOK_NAME,
        "body": PLAYBOOK_CONTENT,
    }
    print(f"Creating playbook '{PLAYBOOK_NAME}'...")
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    if resp.status_code not in (200, 201):
        print(f"ERROR creating playbook: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    playbook_id = data.get("playbook_id") or data.get("id")
    print(f"  Playbook created: {playbook_id}")
    return playbook_id


def create_knowledge_note(headers: dict) -> str:
    url = f"{BASE_URL}/v3/organizations/{DEVIN_ORG_ID}/knowledge/notes"
    payload = {
        "name": KNOWLEDGE_NOTE_NAME,
        "body": KNOWLEDGE_NOTE_CONTENT,
        "trigger": "When working on the datastack-demo-api repository or updating docs/api-reference.md",
    }
    print(f"Creating knowledge note '{KNOWLEDGE_NOTE_NAME}'...")
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    if resp.status_code not in (200, 201):
        print(f"ERROR creating knowledge note: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    note_id = data.get("knowledge_id") or data.get("id")
    print(f"  Knowledge note created: {note_id}")
    return note_id


def create_schedule(headers: dict, playbook_id: str) -> str:
    url = f"{BASE_URL}/v3/organizations/{DEVIN_ORG_ID}/schedules"
    payload = {
        "name": "Nightly API doc sweep",
        "prompt": (
            "Perform a full documentation audit of the datastack-demo-api repository "
            "(https://github.com/turnup4ethan2/datastack-demo-api).\n\n"
            "Read every file in app/routes/ and compare against the current docs/api-reference.md. "
            "Update docs/api-reference.md to accurately reflect ALL current endpoints and open a "
            "draft PR titled \"docs: auto-update API reference\" with a summary table of every "
            "discrepancy found.\n\n"
            "This is a scheduled sweep — check everything, not just recently changed files. "
            "If docs are already accurate, do not open a PR."
        ),
        "playbook_id": playbook_id,
        "frequency": "0 2 * * *",   # nightly at 2am UTC
        "timezone": "America/Los_Angeles",
    }
    print("Creating nightly schedule...")
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    if resp.status_code not in (200, 201):
        print(f"ERROR creating schedule: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    schedule_id = data.get("scheduled_session_id") or data.get("id")
    print(f"  Schedule created: {schedule_id} (nightly at 2am Pacific)")
    return schedule_id


def main():
    for var, name in [(DEVIN_API_KEY, "DEVIN_API_KEY"), (DEVIN_ORG_ID, "DEVIN_ORG_ID")]:
        if not var:
            print(f"ERROR: {name} environment variable is not set.", file=sys.stderr)
            sys.exit(1)

    headers = {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json",
    }

    playbook_id = create_playbook(headers)
    knowledge_id = create_knowledge_note(headers)
    schedule_id = create_schedule(headers, playbook_id)

    print()
    print("=" * 60)
    print("Setup complete. Add these as GitHub repository secrets:")
    print("=" * 60)
    print(f"  DEVIN_API_KEY     = (your existing key)")
    print(f"  DEVIN_ORG_ID      = {DEVIN_ORG_ID}")
    print(f"  DEVIN_PLAYBOOK_ID = {playbook_id}")
    print()
    print("Also created (no action needed):")
    print(f"  Knowledge note : {knowledge_id} — auto-applied to all org sessions")
    print(f"  Nightly schedule: {schedule_id} — full doc sweep at 2am Pacific every night")


if __name__ == "__main__":
    main()
