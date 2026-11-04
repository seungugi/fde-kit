# Decide / 해결 방향

**Start:** Need to choose scope, implementation approach, dependencies or a technical compromise.
**Inputs:** Current evidence-linked specification, stakeholder answers, existing assets, working environment and remaining time.
**Output:** A concise decision in `fde-notes/DECISIONS.md`: source, choice, reason, tradeoff and when to revisit it.

Inspect what already works. Prefer an existing project capability, then a standard/platform feature, then an installed dependency, then small new code. Add a new tool only if it solves a concrete requirement well enough to justify installation, integration and debugging time.

For unresolved output or behavior choices, compare viable alternatives by benefit, cost, risk and fit, then use the [one-question loop](coach.md#one-decision-per-question). Mark the recommendation as advice; the user chooses or explicitly delegates. Do not pad the comparison with artificial options. Internal implementation preserving the agreed result is delegated; respect existing architectural conventions. Do not sacrifice required behavior or validation to shorten code. Identify a thin end-to-end result that can reveal integration risk early.

Tie each comparison to specification IDs and the evidence that makes it relevant. If an option depends on an unknown operational fact, identify the stakeholder question first and mark the option conditional. After a participant choice, update the rule, status, answer source and acceptance in BRIEF together. A reported busy period is context for this decision, not automatic authorization for alerts, staffing or a new deliverable.

Separate mandatory behavior and hard constraints from optional quality improvements. Choose a simple baseline that satisfies the former, then improve the highest-impact confirmed weakness against that baseline. If optimization is mandatory, include a feasible initial optimizer and check its required objective/constraints; do not demote it to optional or claim a global optimum without evidence. Protect time for integration, verification and required submission work. Revisit the approach when a stakeholder answer changes the objective, constraints or failure cases, rather than merely adding another feature.

**Exit:** The user has chosen or delegated the unresolved product choices, the approach meets mandatory conditions, excluded scope is visible, and the riskiest technical assumption has a cheap check.
For a whole-service planning request, connect these choices to the user flow, data, required components, ordered work and acceptance using [Discover's plan closure](discover.md#close-the-interview-with-a-complete-implementation-plan). A chosen algorithm or ready first slice alone does not complete that request. Planning does not authorize product implementation.
**Fallback:** If an approach fails, choose an equivalent internal implementation within delegated scope. If the alternative changes output, behavior or constraints, explain the tradeoff and ask one question before using it. Never silently reduce scope or redefine acceptance to make a test pass.

Ponytail may assist with reuse and minimal complete changes when installed. It is optional; do not load it or other repositories merely to repeat this decision.
