# Decide / 해결 방향

**Start:** Need to choose scope, implementation approach, dependencies or a technical compromise.
**Inputs:** Current evidence-linked specification, stakeholder answers, existing assets, working environment and remaining time.
**Output:** A concise decision in `fde-notes/DECISIONS.md`: source, choice, reason, tradeoff and when to revisit it.

Inspect what already works. Prefer an existing project capability, then a standard/platform feature, then an installed dependency, then small new code. Add a new tool only if it solves a concrete requirement well enough to justify installation, integration and debugging time.

For unresolved consequential business/output choices, compare viable alternatives by benefit, cost, risk and fit, then use the [batched question loop](coach.md#one-decision-per-question). Mark the recommendation as advice; the user chooses or explicitly delegates. Do not pad the comparison with artificial options. Ordinary wording, colors, layout and equivalent internal implementation are delegated by default; respect explicit constraints, accessibility and existing conventions. Do not sacrifice required behavior or validation to shorten code. Identify a thin end-to-end result that can reveal integration risk early.

Tie each comparison to specification IDs and the evidence that makes it relevant. If an option depends on an unknown operational fact, identify the stakeholder question first and mark the option conditional. After a participant choice, update the rule, status, answer source and acceptance in BRIEF together. A reported busy period is context for this decision, not automatic authorization for alerts, staffing or a new deliverable.

Separate mandatory behavior and hard constraints from optional quality improvements. Choose a simple baseline that satisfies the former, then improve the highest-impact confirmed weakness against that baseline. If optimization is mandatory, include a feasible initial optimizer and check its required objective/constraints; do not demote it to optional or claim a global optimum without evidence. Protect time for integration, verification and required submission work. Revisit the approach when a stakeholder answer changes the objective, constraints or failure cases, rather than merely adding another feature.

## Optimization framing and method selection

Apply this only when the requested result requires choosing a best feasible combination, allocation, order, schedule or parameter value. A routine edit or deterministic calculation does not need a new optimization process. Reuse the current BRIEF/specification entries and existing code/tests; no separate model report, algorithm catalog or mandatory solver dependency is needed.

**Frame the model before choosing an algorithm.** Link these items to the original requirement, observed data or confirmed answer; compact prose is enough for a small problem:

- Decisions: what can change, its domain (discrete/continuous), and which quantities are fixed inputs.
- Objective: minimize/maximize what, in which units; preserve explicit priority order between objectives. Do not invent weights, penalties, acceptance gaps or a tradeoff between a hard constraint and a better score.
- Feasibility: hard constraints, boundary inclusivity, resource limits and required behavior when no acceptable result is available. Identify missing facts that can change the model; ask only consequential unresolved questions using the active project/user question policy.
- Scale and representation: measure input sizes and expected variables/constraints; include the cost of deriving distances, eligibility, compatibility or other model inputs. Validate those transformations separately. Candidate reduction, discretization, sampling or rounding changes the searched model; state its scope and error limits.
- Acceptance and budget: required solution quality, independently checkable objective/constraints, available environment and time reserved for generation, verification and delivery. Planning-only requests stop at the plan.

**Recognize structure, then select a method.** Treat familiar families as hypotheses, not permission to drop awkward constraints:

| Structure in the actual requirement | Families worth comparing |
|---|---|
| Select subsets under cost/coverage constraints | Covering, budgeted selection, integer programming |
| Assign items to limited resources | Matching, flow, assignment, integer programming |
| Order dependent work or respect time windows | Scheduling, constraint programming, dynamic programming |
| Choose paths or visit sequences | Graph algorithms, routing, dynamic programming |
| Tune continuous values | Linear/convex optimization when their assumptions hold; otherwise bounded numerical search |

Compare only plausible alternatives by constraint fit, measured scale, solution-quality evidence, implementation risk, runtime/memory and dependency availability. Prefer an existing capability or standard algorithm before custom search. If consulting references, search by the structural family plus the decisive constraints and check that the source's assumptions match. Do not promise runtime from problem size alone or install a framework automatically.

**Start feasible, improve, and stop deliberately.** Within authorized implementation, build a simple valid baseline for the same objective and hard constraints, then improve it if required quality is not yet met. Greedy construction/local improvement can be useful baselines; exhaustive search, dynamic programming or a solver may give stronger bounds or proofs when scale and structure permit. A baseline alone does not satisfy a requirement for proven optimality. Justify pruning, dominance or independent decomposition against every relevant constraint and shared resource; do not assume reductions are safe from a familiar example.

Choose a bounded search/stopping rule that leaves verification time. Preserve the best independently checked feasible result in the existing output/checkpoint location; do not overwrite it with a partial or invalid attempt. Stop safely on timeout or unavailable dependencies and report what is known. Distinguish no feasible result found from proven infeasibility, and distinguish a feasible result from proven optimality within the stated model. Recompare baseline and improvements on the same inputs, constraints and objective, including consequential side effects. Resume an existing search only when the tool supports it and the model/input context still matches.

Use [Verify](verify.md) for result and proof checks, and [Handoff](handoff.md) to preserve the model, incumbent result and remaining uncertainty without adding documents. Reopen only affected entries when the objective, constraints or inputs change; the normal evidence invalidation rules remain in force.

**Exit:** The user has chosen or delegated the unresolved product choices, the approach meets mandatory conditions, excluded scope is visible, and the riskiest technical assumption has a cheap check.
For a whole-service planning request, connect these choices to the user flow, data, required components, ordered work and acceptance using [Discover's plan closure](discover.md#close-the-interview-with-a-complete-implementation-plan). A chosen algorithm or ready first slice alone does not complete that request. Planning does not authorize product implementation.
**Fallback:** If an approach fails, choose an alternative within default presentation/internal or explicit delegation. If it changes business meaning, required behavior, constraints or risk, explain the tradeoff and ask one consequential question before using it. Never silently reduce scope or redefine acceptance to make a test pass.

Ponytail may assist with reuse and minimal complete changes when installed. It is optional; do not load it or other repositories merely to repeat this decision.
