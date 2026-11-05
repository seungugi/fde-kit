---
name: fde-kit
description: Use when a user asks for an FDE workflow, a multi-step field project with explicit deliverables and constraints, or resuming work that already has fde-notes. Use for problem framing, controlled execution, artifact-grounded delivery explanations and handoff; not for ordinary questions or isolated trivial edits.
---

# FDE Kit

Turn an unfamiliar requirement into a working, explainable result through one continuous flow: understand the job → define behavior → implement a complete functional slice → verify it. A module supplies missing guidance, not another interview, plan or approval ceremony.

## Match the request

- Explanation/status/advice: answer from relevant evidence without initializing records or restarting the lifecycle. For a deep explanation of an actual deliverable, use [Explain](references/explain.md); a simple status question stays short. Check live status when the answer depends on verification state.
- Small scoped edit: inspect affected files and requirements, update existing code/tests, and run proportionate checks. No new interview or whole-project plan. Registered-file changes still require current evidence.
- New field task: read the actual task, submission instructions, data and existing project instructions; use [Discover](references/discover.md). The kit's README and examples are not task requirements.
- Resume multi-step work: read BRIEF and DECISIONS, run `python <this-skill>/scripts/fde.py status <project>`, then reconcile HANDOFF if present. Reuse settled answers; an old completion statement is not current verification.

For competition work, first read [profile restrictions](references/profiles.md#competition-restrictions), including Computer Use prohibition and Astra restriction, and [rubric alignment](references/rubric.md). The actual environment and official criteria govern; do not invent weights, hidden tests or scores. Do not apply competition restrictions to standard work automatically.

## One source for each kind of information

| Record | Owns |
|---|---|
| BRIEF or prescribed equivalent | Current requirements with source IDs, business terms, user flow, rules, implementation slices and acceptance |
| DECISIONS | Consequential questions/answers, sources, alternatives, reasons, progress and unresolved operational limits |
| Existing CLI state/evidence/HANDOFF | Task contracts, dependencies, actual verification logs and generated resume snapshot |

Use references between these records. Do not add parallel PRDs, glossaries, tickets or stage reports when the existing records suffice. Update current rules and acceptance together; history alone must not conceal a changed requirement. Brief/contract/file changes retain the existing evidence invalidation rules.

## Follow the flow, load only what is needed

| Need | Guidance | Result |
|---|---|---|
| Interpret task/data and resolve missing business behavior | [Discover](references/discover.md) and its [question policy](references/coach.md#one-decision-per-question) | Evidence-linked specification; only consequential unresolved questions |
| Choose between material implementation approaches | [Decide](references/decide.md) | Reasoned choice in the same specification; no repeated interview |
| Sequence or implement confirmed behavior | [Execute](references/execute.md#functional-slices) | Small, independently demonstrable functional slices |
| Adapt a new small web service | [Web starter](references/web.md) | The same slices connected through UI, server, storage and checks |
| Check a slice, fix or integrated delivery | [Verify](references/verify.md) | Actual evidence plus requirement/implementation review and remaining limits |
| Hand over or deeply understand a substantial result | [Explain](references/explain.md) | Actual mechanism, choices/costs, data/state flow, reproducible checks, failure behavior and claim limits; optional practice |
| Resume the work | [Handoff](references/handoff.md) | Current snapshot reconciled with artifacts, not another lifecycle |

For required optimization, use [model/method selection](references/decide.md#optimization-framing-and-method-selection). For matching table/rule/search outputs, use [execution recipes](references/recipes.md). Neither is mandatory for unrelated work.

The human leads consequential business choices; ordinary wording, layout and equivalent implementation are delegated within explicit requirements, existing design and accessibility. [Coach](references/coach.md) owns the question policy. A planning-only request stops at the plan. An implementation request continues through ready slices and their checks without another phase approval; unresolved decisions block only dependent work. Readiness is not verification. At the handover of a substantial implemented result, use Explain to cover its applicable depth dimensions from current artifacts and evidence without a separate prompt. A library list or completion summary alone is insufficient. Respect explicit depth/time requests, while minor edits remain concise. Practice is optional and only while AI assistance is permitted.

## Local tools and evidence

Initialize only when useful: `python <this-skill>/scripts/fde.py init <project> --profile standard --goal "user's goal"`. Choose `competition` for constrained contest/practice. Core installation contains workflow/record tools; optional recipes and web assets stay in the full repository unless explicitly installed with `init --full`. Do not overwrite a customized installation; see [CLI semantics](references/cli.md).

For a small tracked slice use [add → verify --handoff](references/execute.md#small-single-owner-work). Reuse its task ID with `update` when the same behavior changes. Track relevant input, source, tests and outputs; use `coverage` for registered criteria. A passing command only checks its declared contract, not every requirement or qualitative quality. Do not repeat valid checks just for a new stage record.

Preserve original inputs, user files and verification evidence under the [file reuse rules](references/execute.md#file-reuse-and-temporary-work). Use the available Python executable. Optional [upstream references](references/sources.md) are ideas, not dependencies or authority to install, delegate, contact people, publish, deploy or send data externally. Report outcomes and limits in plain language.
