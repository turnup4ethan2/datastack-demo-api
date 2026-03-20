# datastack-demo-api

Demo repository for DataStack's API — used to demonstrate Devin-powered automatic documentation sync.

**The problem this solves:** Engineers ship new endpoints without updating docs. This repo shows how a single GitHub Actions workflow + Devin session keeps `docs/api-reference.md` in sync automatically, opening a draft PR for human review every time route files change.

---

## Repository Structure

```
app/
  main.py              # FastAPI entry point
  routes/
    users.py           # GET/POST /users, GET/DELETE /users/{id}
    products.py        # GET/POST /products, GET /products/{id}
    orders.py          # POST /orders, GET /orders/{id}, PATCH /orders/{id}/status
docs/
  api-reference.md     # Human-readable API docs (kept in sync by Devin)
scripts/
  setup_devin.py       # One-time setup: creates playbook + knowledge note
  trigger_devin.py     # Called by CI: creates a Devin session when routes change
.github/
  workflows/
    doc-sync.yml       # Triggers on push to main when app/routes/** changes
```

---

## How It Works

1. An engineer pushes a change to any file in `app/routes/`
2. GitHub Actions detects the change and runs `scripts/trigger_devin.py`
3. Devin receives a session with the list of changed files and a playbook instructing it to:
   - Read the changed route files
   - Compare against the current `docs/api-reference.md`
   - Rewrite the docs to reflect the current API
   - Open a draft PR with a summary of what changed
4. An engineer reviews and approves the draft PR — no manual doc writing required

---

## Setup

### Prerequisites

- Python 3.11+
- A Devin API key (Organization/Teams plan)
- A GitHub repository with Actions enabled

### Step 1 — Clone and install dependencies

```bash
git clone https://github.com/your-org/datastack-demo-api
cd datastack-demo-api
pip install fastapi uvicorn requests
```

### Step 2 — Run the one-time Devin setup

This creates the reusable playbook and knowledge note in your Devin org.

```bash
export DEVIN_API_KEY=your_devin_api_key
export DEVIN_ORG_ID=your_devin_org_id
python scripts/setup_devin.py
```

The script prints the IDs you'll need in the next step.

### Step 3 — Add GitHub repository secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `DEVIN_API_KEY` | Your Devin API key |
| `DEVIN_ORG_ID` | Your Devin org ID |
| `DEVIN_PLAYBOOK_ID` | Output from `setup_devin.py` |

### Step 4 — Test the automation

Push any change to a file in `app/routes/` on the `main` branch:

```bash
# Example: add a new field to an existing route
echo "# new comment" >> app/routes/orders.py
git add app/routes/orders.py
git commit -m "feat: add comment to orders route"
git push origin main
```

Watch the **Actions** tab — the workflow will fire, trigger a Devin session, and print the session URL. Within a few minutes, a draft PR will appear with updated docs.

---

## Running the API Locally

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Customizing the Playbook

The playbook content is defined in `scripts/setup_devin.py` in the `PLAYBOOK_CONTENT` variable. After editing it, re-run the script (it will create a new playbook) and update the `DEVIN_PLAYBOOK_ID` secret.

The knowledge note (`KNOWLEDGE_NOTE_CONTENT`) defines DataStack's doc conventions — tone, format, required sections, and auth pattern. It is automatically applied to all Devin sessions in your org.

---

## Why Devin vs. a Static Doc Generator

Static generators (Swagger, mkdocs-gen) extract type signatures. Devin reads the actual implementation — validation logic, error cases, auth middleware, business rules — and writes documentation that reflects how the API *actually behaves*. It can also update conceptual docs, READMEs, and onboarding guides, not just API reference.
