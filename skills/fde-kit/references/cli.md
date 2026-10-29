# CLI reference

Python 3.10+; no package installation. From the package use `python fde.py`. After project initialization use `python .agents/skills/fde-kit/scripts/fde.py`. On Linux, use `python3` if required. Paths containing spaces must be quoted.

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

- `init`: project-local skill copy, a bounded addition to existing AGENTS.md, and records. Repeating unchanged setup preserves existing files; a modified/different skill is a conflict, not an overwrite.
- `launch`: starts the supplied `codex` in the project with a user-led starter prompt. Requires prior init. It uses normal Codex authentication, model and permission settings; it neither installs a CLI nor supplies credentials. `--print-prompt` previews the prompt without starting Codex. If Codex is only a shell alias/function, start it manually in the project with that prompt.
- `criterion`: register/update an ID, title, `--basis official|assumed` and `--source`. Optional `--points` is the documented official maximum, never a prediction. Invalid/unknown points stay unset; assumed points are rejected.
- `coverage`: source-aware task/evidence mapping, with optional `--json`. No estimated score or automatic claim of rubric satisfaction.
- `add`: unique ID, title, acceptance and individual `--files` required. Optional `--depends T1 T2`, `--owner worker-a`, `--criteria R1 R2`. Register criteria before referencing them. Creation order is the default ordering of dependency-ready work; plan that order deliberately.
- `start`: `doing`; dependencies must be currently verified; shared watched files cannot have two active owners.
- `ready`: `implemented`, not verified. Existing proof is not reused to skip a new run.
- `verify`: invokes the actual command without a shell, records a new evidence log, stores snapshots and sets verified/failed. Use `verify --timeout 60 ./project T1 -- ...` with timeout before project/task. Default 120 seconds. A timeout is not success. Use meaningful acceptance checks.
- `status`: current effective statuses; `--json` includes contracts and evidence. Read-only, even if a writer lock exists.
- `intent`: increments goal revision and records the reason. Update BRIEF consistently afterward.
- `handoff`: regenerate the machine-owned snapshot; user-authored handoff files are not overwritten.

State: `todo → doing → implemented → verified`. Failed checks show `failed`; missing verified dependencies show `blocked`; stale earlier proof shows `needs_verification`. Implementation edits happen through ordinary file tools. File/brief/dependency/log changes are detected when status or handoff runs, not by a background watcher.

Exit codes: 0 = command completed (for verify, evidence accepted); 1 = verification ran but failed; 2 = invalid input, conflict or missing prerequisite. State JSON is readable and project-local. This is a lightweight, single-writer record system; it does not sandbox commands or resist intentional evidence tampering.
