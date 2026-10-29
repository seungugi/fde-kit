# Align work to actual assessment criteria

Read the task README, official rubric, required deliverables and relevant platform guidance. Cite the file/section or actual provided statement for each criterion. A general evaluation direction is not a detailed point allocation. Do not search for leaked/hidden tests or claim an unknown grading formula.

## Record provenance

Use `criterion` with `--basis official` for a criterion actually stated by an official source, or `--basis assumed` for the user's/agent's provisional working criterion. `--source` is mandatory. The label records your assertion of provenance; the CLI cannot prove that the cited source supports it. Read and check the source yourself.

Set `--points` only when the official source explicitly gives the maximum points for that item. Unknown points stay unset. Assumed criteria cannot have points. Do not fill a 100-point total by guessing. Use `criterion` again to update an item when the source changes; every registration advances its revision, preserves the previous item in history and makes linked verification stale, even when the title and source location are unchanged. Source text itself is not monitored automatically; declare its local file as a task input when that is useful.

## Connect decisions to evidence

Link a task with `add ... --criteria R1 R2`. Check `coverage` at meaningful milestones, before changing priorities and before submission. It reports:
- `unmapped`: no task is linked to the criterion;
- `needs_evidence`: some linked work is not currently verified;
- `evidence_available`: every linked task has current recorded evidence.

The last label does **not** say the criterion is fully satisfied or award points. Review whether the task set and actual checks cover the whole criterion. A test that checks file existence cannot establish argument quality; a test that only checks samples cannot establish all edge cases.

Suggest prioritizing mandatory deliverables and unmet explicit criteria, with remaining time and implementation risk stated. The user chooses. If no rubric is available, continue useful work against the confirmed task requirements, label provisional criteria clearly and flag the missing rubric once rather than stopping all progress.

Keep real task material and assessment notes in the local project. The reusable public kit repository should contain only generic instructions/examples, never competition submissions, notes or logs. Public availability does not itself establish contest approval.
