# Verify / 검증·통제

**Start:** A fix, deliverable or completion claim needs evidence.
**Inputs:** Original acceptance criteria, current artifacts, test inputs and expected results.
**Output:** A real command log plus the agent's assessment of which acceptance conditions it proves and which remain unchecked.

Use a check derived from the requirement. Include a supplied example, an independently determined expected result and important boundary/failure cases. Test the actual output interface where relevant. A model's repeated agreement or a command that merely prints “OK” proves nothing about correctness.

Review the current slice against its source-linked requirements; do not repeat discovery. Pending decisions must not become test expectations. Check through an observable boundary (HTTP response and stored state, exported output, or domain interface), not private function structure. For a bug/risky rule, first confirm the focused regression fails for the intended reason, then verify the fix; unrelated setup failure is not that evidence.

Before closing a slice or integrated delivery, review two questions in the same pass:
- **Requirement fit:** Do implemented behavior, permissions, states and failures satisfy the confirmed acceptance? Is any required behavior missing or extra behavior unsupported?
- **Implementation quality:** Are validation, persistence, error handling and code boundaries adequate for this scope? Did changes break an already completed path?

Fix material findings and rerun affected checks; do not add a separate report/review ceremony or claim reviewer approval from a test result. Record consequential findings and untested boundaries in DECISIONS. Only delegate a review if independently authorized. For web-specific coverage and manual screen checks use [Web](web.md#acceptance-and-explanation).

Extend existing tests for repeatable checks; use a managed temporary directory for one-off fixtures and probes under the [file rules](execute.md#file-reuse-and-temporary-work). When plausible wrong results are a material risk, challenge the checker with a disposable copy: change one business-critical value while preserving valid syntax and row counts, and confirm it fails. Keep the original output intact and never use the intentional failure as evidence of product success. The full kit's `skills/fde-kit/assets/verification-example/README.md` demonstrates rejection of a partly finished job marked complete despite valid JSON and IDs. It remains in the repository unless installed with `init --full`; running this example is not a prerequisite for checking the actual task. Adapt expected values from requirements; sample cases do not certify another product. Clean up disposable copies after the check while preserving the command log and required failure/regression evidence.

Run `verify` with an argv command after `--`; no shell is inserted. Read the resulting log. A command must finish successfully without changing declared watched files or the brief. Use implementation commands separately if they generate artifacts; verification should inspect those artifacts. A failed process, timeout, missing input or changed file cannot be verified.

For a small single-owner task, use `verify --handoff <project> <id> -- <check command>` for the first real check rather than running it once directly and again only for bookkeeping. Separate `start`/`ready` and a later `handoff` call are unnecessary in this path. Inspect the evidence and current state regardless of the command's exit status.

The CLI stores file SHA-256 hashes, brief hash, goal revision, task contract, dependency evidence IDs, exit code and log hash. Later `status` recomputes validity. Changed files/brief/goal/dependency evidence/log require renewed verification. This is accidental-staleness detection, not a tamper-proof audit or semantic proof. Add every relevant file to the contract, including validation code. Do not edit state JSON to manufacture success.

Each real verification attempt adds an evidence log. Preserve those logs and their referenced artifacts, including failures; this kit has no safe evidence-pruning command. File reuse reduces duplicate working documents and disposable files, not the necessary evidence trail. Do not copy the log into a separate report unless a deliverable requires it.

For a document or analysis, combine executable structural/data checks with a recorded human/agent review against concrete criteria. Report the review's scope and remaining uncertainty; do not claim the CLI proved qualitative quality.

For [execution recipes](recipes.md), require row accounting and independently calculated business expectations, not just a successful generation command or manifest hashes. Include the configuration, source files, checker, generated artifacts and relevant recipe code in `--files`. A new file added to a document directory is not detected by hashes of previously declared files: reconcile the current inventory before reusing evidence and update the task contract when it changes. Verify citations against the actual file and line span. Review source authority, contradictions and freshness yourself; lexical matches do not establish an answer.

For optimization results, independently recompute feasibility and the objective from the original inputs and stated rules, including any transformed eligibility/cost data; do not merely re-read the optimizer's score. Use small exhaustive cases or hand-derived expectations where useful, and exercise material boundary/infeasible/interrupted-search cases. Compare alternatives on the same model and disclose side effects. Report feasible, proven optimal, proven infeasible or unresolved according to actual evidence; a search timeout without a result is not an infeasibility proof. State bounds/gaps only when their derivation, units, direction and model scope are valid. An optimum over sampled candidates is not automatically a global optimum of the original problem. If proven optimality is required, a feasible-only result remains incomplete.

A solver may stop at its own time limit with a valid incumbent that a separate checker can accept if the task permits that quality. This does not change the CLI rule: a timed-out/failed verification command is failed, never verified. Declare relevant model settings, input/transformation code, result and independent checker in the existing contract; retain the actual evidence without a new optimization report.

**Exit:** Current evidence supports the acceptance conditions; important limits are stated. Run the necessary integration check after combining independently tested work.
**Fallback:** After two repetitions of the same failure without new evidence, stop blind retries and investigate the cause. Change the hypothesis, collect a missing observation or reduce optional scope. This is a recommended investigation trigger, not permission to abandon mandatory work.

Timeout stops the directly launched verification process. Avoid commands that start background servers; child daemons are not a managed lifecycle in this kit. This kit does not enforce the environment's network restrictions.
