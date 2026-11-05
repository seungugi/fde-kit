# CLI reference

Python 3.10+; no package installation. From the package use `python fde.py`. After project initialization use `python .agents/skills/fde-kit/scripts/fde.py`. On Linux, use `python3` if required. Paths containing spaces must be quoted.

Default `init` installs the workflow/record CLI without optional recipe code or runnable examples. To add these when needed, run `python <full-kit>/fde.py init <project> --full` from the matching full repository. A core-only installed CLI cannot provide missing assets. No network downloads occur. Core and full use identical state and verification semantics; these installation choices are independent of standard/competition profiles.

New projects receive the current default-delegation guidance in the managed AGENTS block. Existing AGENTS content is preserved by `init`. During an explicitly requested upgrade, inspect that block for older instructions requiring every cosmetic choice to be asked; reconcile only conflicting kit guidance with the user's current preferences while preserving unrelated project instructions. Reinitialization alone does not migrate an old block.

Execution recipes are separate: use the full package's `recipes.py`, or the installed `scripts/recipes.py` after `init --full`. See [recipe contracts and examples](recipes.md). They generate outputs; `fde.py verify` records a separate acceptance check.

Small single-owner deliverables needing tracked verification: after `init` and a short brief, `add` the deliverable, implement it, then run `verify --handoff ./project T1 -- python check_report.py`. Ordinary explanations and trivial edits do not require initialization or this sequence; use SKILL's request routing. Existing registered-file changes still invalidate evidence and require relevant verification. Keep the full sequence below for coordinated work. Existing commands and schema-1 records remain supported.

```bash
python fde.py init ./project --profile competition --goal "Prioritize support requests"
python fde.py launch ./project
python fde.py criterion ./project R1 "Required ordering behavior" --basis official --source "Task README: output rules"
python fde.py add ./project T1 "Order requests" --acceptance "Newest state, urgency then received time" --files queue.py input.csv test_queue.py --criteria R1
python fde.py start ./project T1
python fde.py ready ./project T1
python fde.py verify ./project T1 -- python -m unittest -v
python fde.py status ./project
python fde.py coverage ./project
python fde.py handoff ./project
python fde.py intent ./project --goal "Include reopened requests" --reason "User clarified the workflow"
```

- `init`: core project-local skill copy, a bounded addition to existing AGENTS.md, and records. `--full` includes optional recipe code and examples. Matching core→full installation only adds missing optional files; it preserves existing files, state and evidence. Repeating default init on an existing full copy keeps its optional files. Modified/different/partial installations remain conflicts, not overwrites; upgrade versions by review and explicit replacement as before.
- `launch`: starts the supplied `codex` in the project with a user-led starter prompt. Requires prior init. It uses normal Codex authentication, model and permission settings; it neither installs a CLI nor supplies credentials. `--print-prompt` previews the prompt without starting Codex. If Codex is only a shell alias/function, start it manually in the project with that prompt.
- `criterion`: register/update an ID, title, `--basis official|assumed` and `--source`. Optional `--points` is the documented official maximum, never a prediction. Invalid/unknown points stay unset; assumed points are rejected.
- `coverage`: source-aware task/evidence mapping, with optional `--json`. No estimated score or automatic claim of rubric satisfaction.
- `add`: unique ID, title, acceptance and individual `--files` required. Optional `--depends T1 T2`, `--owner worker-a`, `--criteria R1 R2`. Register criteria before referencing them. Creation order is the default ordering of dependency-ready work; plan that order deliberately.
- `update`: change an existing task using `update <project> <id> --reason "..."` and at least one of `--title`, `--acceptance`, `--files`, `--depends`, `--owner`, `--criteria`. Omitted fields stay unchanged. Supplied lists replace the old list; empty `--depends` / `--criteria` clears that list, while `--files` needs at least one file. The ID, attempts and evidence logs are preserved; actual changes add a before/after history entry. Unknown tasks/criteria/dependencies, cyclic dependencies, escaping/record paths, active ownership conflicts and writer locks are rejected before saving. A task left `verifying` needs inspection before update.
- `start`: `doing`; dependencies must be currently verified; shared watched files cannot have two active owners.
- `ready`: `implemented`, not verified. Existing proof is not reused to skip a new run.
- `verify`: invokes the actual command without a shell, records a new evidence log, stores snapshots and sets verified/failed. Dependencies and overlap with another active task's watched files are checked even without `start`. Use `verify --timeout 60 ./project T1 -- ...` with timeout before project/task. Default 120 seconds. A timeout is not success. Use meaningful acceptance checks.
- `verify --handoff ./project T1 -- ...`: refreshes the snapshot after success, failed execution, timeout or a command-start failure. The verification exit code remains 0/1. Invalid input or a conflicting user-owned HANDOFF is rejected with 2 before the check starts; that prior handoff is preserved. Put `--handoff` and `--timeout` before project/task, not in the command after `--`. If snapshot writing itself fails, the error is reported and the already saved verification evidence remains; rerun `handoff` after resolving the file problem.
- `status`: current effective statuses; `--json` includes contracts and evidence. Read-only, even if a writer lock exists.
- `intent`: increments goal revision and records the reason. Update BRIEF consistently afterward.
- `handoff`: regenerate the machine-owned snapshot; user-authored handoff files are not overwritten.

## Update the same task after a requirement change

Update BRIEF when the requirement changes, then update the affected contract **before** running its next verification. Use `add` only for a new independently checkable deliverable, not to replace an existing ID.

```bash
python fde.py update ./project T1 --acceptance "R1 and the new R2 boundary cases" --reason "User clarified R2"
# If the watched files change, provide the complete new list with --files.
# Implement the changed rule and its checks, then verify the current result once.
python fde.py verify --handoff ./project T1 -- python check_report.py
```

Changes to title, acceptance, files, dependencies or criteria advance a task-local contract revision. An old verified task and its verified dependents become `needs_verification`; reverting the values does not revive the old proof. Same-value updates do not write history or invalidate evidence. Changing only `--owner` records ownership without invalidating an otherwise current check. These exceptions do not restore evidence already invalidated by files, BRIEF, dependencies or other changes. Failed checks remain failed until verification succeeds; the update command never marks work verified.

The additive revision field retains schema-1 compatibility with existing records/proofs in this CLI. Keep `history` and evidence intact; use the current CLI after upgrading. `update` does not edit BRIEF, implement code, run tests or refresh HANDOFF automatically. Use `verify --handoff` after implementation, or `handoff` when only a current snapshot is needed.

State: `todo → doing → implemented → verified`. Failed checks show `failed`; missing verified dependencies show `blocked`; stale earlier proof shows `needs_verification`. Implementation edits happen through ordinary file tools. File/brief/dependency/log changes are detected when status or handoff runs, not by a background watcher.

The small-work path can move from `todo` to `verifying` and then `verified`/`failed` directly. It uses the same evidence rules. Progress notes in DECISIONS do not invalidate evidence; changed requirements still belong in BRIEF and/or the task contract and require fresh checks. Automatic invalidation is intentionally not based on guessing whether a BRIEF edit was merely cosmetic.

Exit codes: 0 = command completed (for verify, evidence accepted); 1 = verification ran but failed; 2 = invalid input, conflict or missing prerequisite. State JSON is readable and project-local. This is a lightweight, single-writer record system; it does not sandbox commands or resist intentional evidence tampering.
