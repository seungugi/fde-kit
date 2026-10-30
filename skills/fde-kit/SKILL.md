---
name: fde-kit
description: Use when a user asks for an FDE workflow, a multi-step field project with explicit deliverables and constraints, or resuming work that already has fde-notes. Use for problem framing, controlled execution and handoff; not for ordinary questions or isolated trivial edits.
---

# FDE Kit

Move an unfamiliar problem to an explainable, verified deliverable. Preserve the user's scope. Use only the module needed now; do not run six ceremonies for every request.

## The human leads

Use [user-led coaching](references/coach.md). The user chooses the direction, priorities and scope. Surface gaps, challenge weak assumptions with reasons and recommend a concrete next step. Perform the currently requested work fully, including checks; do not jump from a request for diagnosis or advice to implementing the whole project. Do not ask again for permission already given for that step.

At the start or resumption of competition work, read the [competition restrictions](references/profiles.md#competition-restrictions) before choosing tools or models, including the prohibition on Computer Use at every stage and the Astra restriction. Also read [rubric alignment](references/rubric.md). Use the actual supplied criteria. When none are available, report that gap and keep useful working criteria labeled as assumptions. Never invent official weights, hidden tests or predicted scores.

## First action

Read the original task and the project's existing instructions. If `fde-notes/state.json` exists, read `fde-notes/BRIEF.md` and run `python <this-skill>/scripts/fde.py status <project>`. Read HANDOFF.md if it exists, as a snapshot to reconcile with current files. New projects have no handoff yet; fill the brief rather than treating its absence as an error. An old “done” statement is not current verification.

For a new project, initialize only when useful: `python <this-skill>/scripts/fde.py init <project> --profile standard --goal "user's goal"`. Choose `competition` only for a constrained contest/practice. Read [profiles](references/profiles.md) for that environment. Initialization is local, with no account connection or external download.

## Select one module

| Situation | Read | Exit evidence |
|---|---|---|
| Success or constraints are unclear | [Discover](references/discover.md) | A short brief with checkable outcomes and labeled assumptions |
| Several approaches or dependencies are possible | [Decide](references/decide.md) | One chosen approach with reason and excluded scope |
| Work needs sequencing or independent owners | [Execute](references/execute.md) | Task contracts and working deliverables |
| A result, fix or completion needs checking | [Verify](references/verify.md) | Actual evidence tied to the current task and files |
| Intent changed, session resumed or context is crowded | [Handoff](references/handoff.md) | Current state, decisions and one next action |
| Someone must operate or explain the output | [Explain](references/explain.md) | Reproducible use instructions and understood limitations |

## Operating rules

- Original requirements and newer user decisions govern. Label your own assumptions; never turn an example into a universal requirement.
- Clarify only decisions that materially change correctness, scope or irreversible actions. Continue independent authorized work. Do not insert routine approval stops.
- Keep one authoritative brief and task list. Reuse existing task documents where required; avoid maintaining competing plans in several frameworks.
- Map relevant work to registered criteria and use `coverage` to identify missing evidence. Coverage is not a grade. The user decides whether to accept a suggested priority change.
- Separate `implemented` from `verified`. The CLI only establishes that a command passed against declared files. You must still assess whether the command tests the acceptance criteria and whether declared files cover relevant inputs, tests and outputs.
- Use the available Python executable (`python3` on many Linux systems). Commands and state semantics: [CLI reference](references/cli.md).
- Optional upstream skills can improve a module if installed; the kit works without them. Read [sources](references/sources.md) only when choosing such additions. Do not install or enable a full framework automatically.
- The kit does not grant permission to contact people, publish, deploy, import private material or send data to external services. Follow the active task and environment rules.

Tell the user the relevant outcome or blocker in plain language. Keep records concise, and do not claim checks you did not run.
