# Verify / 검증·통제

**Start:** A fix, deliverable or completion claim needs evidence.
**Inputs:** Original acceptance criteria, current artifacts, test inputs and expected results.
**Output:** A real command log plus the agent's assessment of which acceptance conditions it proves and which remain unchecked.

Use a check derived from the requirement. Include a supplied example, an independently determined expected result and important boundary/failure cases. Test the actual output interface where relevant. A model's repeated agreement or a command that merely prints “OK” proves nothing about correctness.

Run `verify` with an argv command after `--`; no shell is inserted. Read the resulting log. A command must finish successfully without changing declared watched files or the brief. Use implementation commands separately if they generate artifacts; verification should inspect those artifacts. A failed process, timeout, missing input or changed file cannot be verified.

The CLI stores file SHA-256 hashes, brief hash, goal revision, task contract, dependency evidence IDs, exit code and log hash. Later `status` recomputes validity. Changed files/brief/goal/dependency evidence/log require renewed verification. This is accidental-staleness detection, not a tamper-proof audit or semantic proof. Add every relevant file to the contract, including validation code. Do not edit state JSON to manufacture success.

For a document or analysis, combine executable structural/data checks with a recorded human/agent review against concrete criteria. Report the review's scope and remaining uncertainty; do not claim the CLI proved qualitative quality.

For [execution recipes](recipes.md), require row accounting and independently calculated business expectations, not just a successful generation command or manifest hashes. Include the configuration, source files, checker, generated artifacts and relevant recipe code in `--files`. A new file added to a document directory is not detected by hashes of previously declared files: reconcile the current inventory before reusing evidence and update the task contract when it changes. Verify citations against the actual file and line span. Review source authority, contradictions and freshness yourself; lexical matches do not establish an answer.

**Exit:** Current evidence supports the acceptance conditions; important limits are stated. Run the necessary integration check after combining independently tested work.
**Fallback:** After two repetitions of the same failure without new evidence, stop blind retries and investigate the cause. Change the hypothesis, collect a missing observation or reduce optional scope. This is a recommended investigation trigger, not permission to abandon mandatory work.

Timeout stops the directly launched verification process. Avoid commands that start background servers; child daemons are not a managed lifecycle in this kit. This kit does not enforce the environment's network restrictions.
