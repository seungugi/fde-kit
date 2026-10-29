# Execute / 작업 분해·위임

**Start:** The next result is defined but needs several steps or separate owners.
**Inputs:** Brief, decision, current task statuses, tool availability and deadline.
**Output:** Small task contracts and implemented results; `implemented` is not `verified`.

Break work at independently checkable outputs, not arbitrary file counts. Put a working end-to-end path early. Order mandatory prerequisites first, then high-value work that fits remaining time. Record task IDs, acceptance, dependency IDs, individual watched file paths and owner using the CLI. Watch source data, implementation, meaningful tests and relevant deliverables; undeclared dependencies cannot be invalidated automatically.

Use [delegation contract](../assets/DELEGATION.md) for actual independent work. State editable files separately from watched inputs: several tasks may read one input, but they should not concurrently write the same file. CLI `start` conservatively prevents shared watched-file ownership; run such tasks sequentially if it blocks.

Delegate only if the current environment provides and authorizes agents. A skill never creates delegation authority. Start with a primary implementer and a bounded independent check when useful. If agents are unavailable, execute the same contracts sequentially. Do not simulate agent messages or results.

The primary agent owns the brief, task list and integration. Workers return changed files, commands actually run, results and limits. Inspect changes and rerun meaningful integration checks before accepting them. Update CLI records sequentially; the state lock protects CLI writers, not arbitrary source edits.

**Exit:** Task output exists, declared inputs/outputs are accurate, and it is ready for verification.
**Fallback:** Stop repeatedly dispatching unclear work. Tighten the contract, inspect one failing case and reassign or implement sequentially. Protect the final submission buffer.
