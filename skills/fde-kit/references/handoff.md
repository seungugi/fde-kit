# Handoff / 의도 갱신·맥락 복구

**Start:** Session change, meaningful user correction, a completed work unit, or repeated confusion about current state.
**Inputs:** Current brief and artifacts, real verification evidence, decisions and changed user intent.
**Output:** A regenerated `fde-notes/HANDOFF.md`, plus maintained BRIEF and DECISIONS. Do not create summaries every turn.

For small tasks, `verify --handoff <project> <id> -- <check command>` records the check and refreshes this snapshot together, including a failed check. Keep BRIEF stable unless requirements change; put progress and rationale in DECISIONS. These notes do not invalidate evidence on their own, so never hide changed requirements there to preserve a green status.

When the goal changes, run `intent --goal ... --reason ...` and update BRIEF consistently. The goal revision invalidates previous verification; keep old decisions as history, not active instructions. When a constraint or acceptance detail changes, edit BRIEF and the affected task contract before implementation. Brief edits also invalidate earlier evidence. For this initial kit, task-contract edits are deliberate JSON edits while no CLI writer is active; run status afterward. IDs stay unique; do not recycle completed IDs for unrelated work.

Generate HANDOFF only after status reflects current files. The CLI emits effective states, acceptance, ownership, paths, last command/log, attempts and the next dependency-ready task. Keep rationale, failed approaches and unresolved limitations in DECISIONS. Refer to their source; do not copy entire chat transcripts.

For execution recipes, record which input/schema/rule version and output run directory are current, how exclusions/review rows were handled, and what evidence was missing. A recipe's result or manifest does not replace the independent verification log. Reconcile the source-file inventory on resume; undeclared new documents are outside file-hash tracking.

On resume, read the original task, BRIEF and DECISIONS, run status, then use HANDOFF. A file can remain labeled `verified` in stored state while its effective status is `needs_verification`; always use effective status. Check current artifacts instead of trusting the snapshot or another agent's completion claim.

For a result someone must regenerate or maintain, leave a short operational note in the existing README or DECISIONS: who updates the source and generates/delivers the result, on which available environment, at what time/trigger, and how the recipient distinguishes current from stale output. Record unknowns and the next check; do not invent an owner, installation approval or live-operation readiness. A working prototype can be handed off with these limits. Do not require this ceremony for a one-off answer.

**Exit:** A new session can identify the current goal, what is actually verified, what changed, the main unknown and one useful next action.
**Fallback:** If the snapshot contradicts the original task/current files, surface the conflict and rebuild from those sources. If a lock remains after interruption, inspect its PID and the verification process before removing that specific lock; never delete it automatically.
