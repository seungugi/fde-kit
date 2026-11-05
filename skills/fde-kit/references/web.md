# Optional web starter

Use this for a new small web application when the user accepts this default stack. Preserve an existing project's framework and explicit user choices. Read the original task and data first; a starter is a delivery mechanism, not its requirements or rubric. Report-only and CLI tasks do not acquire a website.

## Default and creation

FastAPI + Jinja2 HTML/CSS + HTMX + SQLite, with pytest/TestClient. A single Python server validates requests and roles, performs business rules, stores records and renders pages or HTML fragments. Complex client-side editing or high write concurrency may justify another stack; explain the tradeoff instead of imposing this default.

From the full kit repository:

```text
python web.py init ./my-webapp
```

The destination must not exist. This copies local assets and installs the project-local FDE workflow; it does not install packages, start servers or deploy. Follow the generated README. In an existing project, adapt relevant starter files to the required layout without overwriting user work or original inputs. A generated README does not replace the original assignment.

Core installations include this guide and scripts/web.py but omit web assets. Use the matching full repository, or explicitly install with `fde.py init PROJECT --full`. Core copies cannot download missing assets. A full installed skill can run `python .agents/skills/fde-kit/scripts/web.py init NEW_PATH`.

## From requirements to a working service

Use the existing BRIEF's terms, flow and [functional slices](execute.md#functional-slices); do not start another web-design interview or copy the plan into a PRD. For each confirmed behavior connect actor/action, page or fragment, request/response, stored entity/state, permission and visible success/failure. Reuse the requirement ID in acceptance and test names/descriptions where useful.

Implement a slice across the existing starter files, then exercise its HTTP/storage behavior before adding the next. For example, if saving an item is required: form submission → validation/role check → commit → visible saved value after reopening; derive duplicate/empty-input behavior from the actual requirements. The example does not prescribe fields, roles or policy for another service.

If a consequential interaction is unclear, a small authorized prototype can resolve that specific question; it is not a delivered feature or a reason to scaffold multiple competing apps. Record the chosen behavior in the same BRIEF and adapt the existing implementation. Keep terminology consistent between labels, data fields, errors and checks.

## Rules and boundaries

Keep HTTP handlers, business functions, persistence and templates separate. Retain pinned dependencies and local static assets; keep databases and secrets out of Git. The generic item board is a working example, not a required feature. Adapt it to the requested product and remove unrelated demo functionality.

Confirm consequential rules from the task and user answers: eligibility, duplicate handling, state transitions, edit rights and conflicting updates. Demo behavior does not establish the target project's business rules.

The user/role switch is a local demo capability gated by DEMO_MODE=1, not real authentication or SSO. Public use needs the environment's authorized identity integration. Without it, protected mutations stay disabled outside demo mode. Preserve server role checks, CSRF and validation when editing views.

## Acceptance and explanation

For each slice test confirmed behavior through HTTP and stored state. Cover relevant persistence after app recreation, duplicate requests, malformed input, role denial, stale edits and rollback; do not invent new product rules to satisfy a generic checklist. Recalculate required totals from source rows. For required optimization, validate constraints independently and label heuristics; validity does not prove optimality. After joining slices, check a complete user journey and affected earlier paths using [Verify](verify.md).

TestClient success does not prove HTMX swaps or browser layout. In authorized local practice inspect actual pages and an interaction. Competition's automated-UI prohibition still applies: the participant performs screen checks, separate from permitted terminal tests. Report checks that were not performed.

`verified` records a declared check passing. Before delivery inspect actual required screens, outputs, failures and the final explanation. Record who reviewed (agent or human), how, and the evidence; an agent review is not human approval. Keep this in existing BRIEF/DECISIONS or the required report, not a fabricated score.

Explain why the stack fits, trace one real input through code/storage/output, identify enforced rules, give runnable checks and limitations. The generated README is an example and must match actual behavior after adaptation.
