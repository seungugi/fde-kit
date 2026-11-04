# Execute / 작업 분해·위임

**Start:** The next result is defined but needs several steps or separate owners.
**Inputs:** Brief, decision, current task statuses, tool availability and deadline.
**Output:** Small task contracts and implemented results; `implemented` is not `verified`.

Start from the required input→processing→usable result path in the existing project. Include interaction, persistence and delivery only as required by the task. Establish a working baseline before optional optimization or visual polish; do not defer mandatory validation, capacity, access or other hard constraints. Check the critical assumption early, then test the complete path when connected. Reuse still-valid evidence rather than rerunning checks solely to record a phase.

Use the file rules below for new work and follow-up requests. CLI state, evidence and handoff are generated records, not extra documents the user must author.

## File reuse and temporary work

- Locate the relevant existing code, tests, outputs and documents before adding a file. Update them for the new requirement; do not create a new project folder, numbered variant or parallel implementation for each request. Use Git history when available for source versions. Keep an isolated checkout or backup only when a concrete recovery or comparison need warrants it.
- Keep current requirements and the implementation plan in the same BRIEF (or prescribed equivalent), answer/decision history in DECISIONS, and regenerate the same HANDOFF. Preserve the task's original README and input data. Update existing editable usage documentation where needed. Explanation, status and review requests normally receive a conversation response; do not create summary, analysis, review or plan documents unless required or explicitly requested. Keep records concise; do not paste the whole conversation into them.
- Add a durable file for a required input/deliverable, a distinct source/test responsibility or a reusable tool with a concrete purpose. Extend the existing test suite before adding standalone check scripts. Do not pre-create empty modules, future extension layers or duplicate plans. Preserve useful code separation; do not impose an arbitrary file-count cap or ask permission for each justified file.
- Use a managed temporary directory for one-off probes, disposable fixtures and experimental outputs. Before cleanup, confirm the resolved path stays inside the agent-created temporary directory and that it contains no required deliverable, user-owned input or registered verification evidence. Clean up the agent's disposable work when finished, including failure paths. Keep only the smallest reusable regression case or required failure evidence in its existing test/log location; if cleanup is incomplete, report the exact leftover rather than silently accumulating it. Do not sweep unrelated files by name, extension or age.
- Maintain one current deliverable at its agreed path where the format/tool permits safe replacement. Update source/input/expectations first, then regenerate and verify the output. Required snapshots, user backups and immutable runs are exceptions. Recipes retain their no-overwrite rule: use temporary runs for exploration and retain a deliberate final run; do not bypass manifests or delete recorded runs to reduce the count. See [recipes](recipes.md).
- Before handoff, inspect files added during this work. Each retained file should have a required output, source/test or reusable-tool purpose. Remove only disposable files this work created under the cleanup boundary above; do not remove user work, required source separation, state, logs, manifests or artifacts referenced by verification. Do not rerun valid checks just to produce another stage record. Unrelated historical cleanup is a separate task.

Apply the [one-question loop](coach.md#one-decision-per-question) before encoding an unresolved consequential business/output rule in code, content or a test expectation. Ordinary wording, colors, layout and equivalent internal implementation are delegated by default. Continue independent authorized work while waiting for a necessary answer. An implementation request does not authorize guessing a missing business rule.

Use the current specification entries as the work contract. Before implementing a unit, check that its mandatory requirements have sources, data implications are supported, stakeholder reports are distinguished from measurements, relevant questions are resolved or delegated, and acceptance matches the selected behavior. Reference its specification IDs in the task's acceptance text and watch the source documents. This review is the agent's responsibility; CLI `status` does not parse or certify the specification.

## Small single-owner work

Use this path for one independently checkable deliverable owned by one agent that needs tracked verification. Simple explanations and trivial edits use SKILL's lighter routing; they do not require new records or a full task contract. For a tracked deliverable, a short paragraph or a few bullets in BRIEF can cover the user/job, input→output, constraints and concrete expected cases. Reference existing requirements rather than copying them. Keep consequential question/answer history, delegation exceptions and operational unknowns in DECISIONS; do not record each routine styling choice.

Register the task before implementation. A follow-up within the same deliverable/acceptance boundary updates its existing task contract and files; create another task only for a distinct independently checkable result. Changed requirements still invalidate earlier verification. Declare relevant source/input, checker and delivered output files; future output files can be registered before they exist. When BRIEF references requirements in another file, watch that file too. Group files into one task when they share one acceptance check, not one task per file. After producing the output, run the real check once through the CLI:

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
