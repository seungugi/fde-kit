# Execute / 작업 분해·위임

**Start:** The next result is defined but needs several steps or separate owners.
**Inputs:** Brief, decision, current task statuses, tool availability and deadline.
**Output:** Small task contracts and implemented results; `implemented` is not `verified`.

## Small single-owner work

Use this path for one independently checkable deliverable owned by one agent. A short paragraph or a few bullets in BRIEF can cover the user/job, input→output, constraints and concrete expected cases. Reference existing requirements rather than copying them. Put only consequential choices or operational unknowns in DECISIONS; separate interview/plan/explanation documents are optional.

Register the task before implementation. Declare relevant source/input, checker and delivered output files; future output files can be registered before they exist. When BRIEF references requirements in another file, watch that file too. Group files into one task when they share one acceptance check, not one task per file. After producing the output, run the real check once through the CLI:

```bash
python fde.py add ./project T1 "Deliver report" --acceptance "BRIEF expected cases" --files input.csv report.py check_report.py result.json
# Implement and generate result.json using the project's actual tools.
python fde.py verify --handoff ./project T1 -- python check_report.py
```

`start` and `ready` are optional bookkeeping for this path. Verification still checks prerequisites, active watched-file ownership, unchanged files/brief and the command result. `--handoff` writes the current snapshot on success or failure; it never converts a failed check into success. No new profile or weaker verification mode is introduced. On a requirement change or resume, use the same status/handoff rules below and in the handoff module.

## Coordinated work

Break work at independently checkable outputs, not arbitrary file counts. Put a working end-to-end path early. Order mandatory prerequisites first, then high-value work that fits remaining time. Record task IDs, acceptance, dependency IDs, individual watched file paths and owner using the CLI. Watch source data, implementation, meaningful tests and relevant deliverables; undeclared dependencies cannot be invalidated automatically.

Use [delegation contract](../assets/DELEGATION.md) for actual independent work. State editable files separately from watched inputs: several tasks may read one input, but they should not concurrently write the same file. CLI `start` conservatively prevents shared watched-file ownership; run such tasks sequentially if it blocks.

Delegate only if the current environment provides and authorizes agents. A skill never creates delegation authority. Start with a primary implementer and a bounded independent check when useful. If agents are unavailable, execute the same contracts sequentially. Do not simulate agent messages or results.

The primary agent owns the brief, task list and integration. Workers return changed files, commands actually run, results and limits. Inspect changes and rerun meaningful integration checks before accepting them. Update CLI records sequentially; the state lock protects CLI writers, not arbitrary source edits.

**Exit:** Task output exists, declared inputs/outputs are accurate, and it is ready for verification.
**Fallback:** Stop repeatedly dispatching unclear work. Tighten the contract, inspect one failing case and reassign or implement sequentially. Protect the final submission buffer.
