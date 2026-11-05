# FDE Web Starter

FastAPI + Jinja2 + HTMX + SQLite, with pytest. This small persistent item board exercises create/list/delete and is meant to be adapted to the actual task. Python 3.10+ is required by the web dependencies; the pinned dependency set was tested on Python 3.12 on Windows. It is not a production identity service.

## Run locally

Create an isolated environment and install the pinned dependencies. No packages are installed by the scaffold command.

```bash
python -m venv .venv
# Linux/macOS
.venv/bin/python -m pip install -r requirements.txt
DEMO_MODE=1 .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DEMO_MODE = "1"
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Open http://127.0.0.1:8765. Keep the process running while using the app. Stop it with Ctrl+C. Use a different free port if 8765 is occupied. `/health` is a process health check, not proof that every feature works.

DEMO_MODE=1 enables fictional-user switching on the local interface. It does not verify who the visitor really is. Without demo mode protected mutations are disabled pending integration with an authorized identity provider. Do not expose the demo user switch as public login. Set APP_DB to override the database path and APP_SECRET to supply a session secret; keep secrets and database files out of Git. The default local database survives server restart; sessions may be reset when using a process-random secret.

## Adapt one behavior at a time

Read the actual task and update `fde-notes/BRIEF.md`: requirement/source → actor action → page/request → stored result → expected visible outcome. Record consequential answers in DECISIONS. Use the installed workflow's `references/web.md` and `references/execute.md#functional-slices`; do not start a separate web specification.

Build one complete required behavior across routes, storage and templates, with its HTTP/storage check. Reuse its task ID for follow-up changes. Replace unrelated item-board behavior rather than treating it as a requirement. Whole-service completion also needs the remaining required flows and an integration check. The demo role switch remains a demo; this workflow does not add real authentication.

## Inspect and test

Use the virtual environment's Python:

```text
python -m pytest tests -q --basetemp .test-tmp
python .agents/skills/fde-kit/scripts/fde.py status .
```

The task's original README/data and user choices remain authoritative. Update the project BRIEF/DECISIONS before consequential implementation. For a registered deliverable use `fde.py verify --handoff . TASK_ID -- <venv-python> -m pytest tests -q --basetemp .test-tmp` with the actual task ID and watched inputs/code/tests/output files. Tests do not replace a permitted browser interaction and visual review.

## Structure and explanation

`app/main.py` creates the application, sessions and static/template handling; `app/features.py` implements task routes; `app/db.py` and `app/security.py` handle storage and request safeguards. `templates/` describes HTML, `static/` supplies local styling and HTMX. Keep domain calculations in separate Python functions when adapting this starter.

Trace a submitted value through validation, business logic, SQLite commit and returned HTML. Explain actual checks and remaining limits. A successful command is not a human review or automatic submission-ready certification.

HTMX 2.0.8 is vendored from https://github.com/bigskysoftware/htmx/tree/v2.0.8 with its Zero-Clause BSD license in static/htmx.LICENSE. Its minified file SHA-256 is 22283ef68cb7545914f0a88a1bdedc7256a703d1d580c1d255217d0a50d31313. No runtime CDN is required.
