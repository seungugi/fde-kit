# Explain / 결과물 기반 심층 설명·인수인계

**Start:** Handover of a substantial implemented result, a request to understand an existing deliverable, or permitted preparation for personally explaining it. A small edit or status question needs only the relevant explanation, not a full lesson.
**Inputs:** Actual task/BRIEF, current code and outputs, data/settings, DECISIONS and valid verification evidence.
**Output:** An artifact-grounded explanation in the conversation, followed by optional understanding practice. Use the [delivery outline](../assets/EXPLAIN.md) for a requested/required document; update existing documentation instead of generating another report each time.

## Ground the explanation before teaching

Inspect the actual implementation and results, not just README claims or the intended plan. For tracked work, reconcile current CLI status with the input/code/output version and logs. Reuse valid evidence; do not rerun checks merely to write an explanation. If artifacts are missing, request their location and explain only the accessible parts. Never substitute the kit's demo for the user's deliverable.

Attach consequential claims to an existing file/function, requirement/decision ID, data row/key, output field or verification log. Inspect line numbers before citing them. Distinguish implemented behavior, observed execution, recorded intent, assumptions, missing functionality and proposed improvements. Code can show a branch exists; only matching execution evidence shows it was exercised. A dependency being installed does not establish that a feature uses it.

Keep recorded design reasons separate from retrospective inference. If no reason was recorded, say so and describe a plausible technical rationale as inference, not as the user's earlier choice. A comparison can explain an alternative without claiming it was implemented or benchmarked. Treat supplied question examples as source material for desired depth, not as proof that their premise, domain, metric or architecture applies to this project. Keep private task/question material and filled explanations in the authorized project; the public kit contains only general guidance.

## Explain the actual result in depth

Start with the solved problem, current completion boundary and a compact flow diagram/table when useful. Then cover the following dimensions at a depth proportional to the delivered work. Connect technical terms to this project's behavior before naming libraries or algorithms. Do not substitute a generic technology tutorial for the explanation.

### Mechanism, choice and cost

For consequential design choices, explain the steps or rules that produce the result, the requirement/data evidence they address, a viable alternative and the concrete tradeoff. Compare behavior under the same constraints; use a small labeled example if it makes the difference clear. Separate a real project example from a hypothetical illustration. Discuss sacrificed quality, implementation/runtime/storage cost or operating complexity where relevant; do not claim measured superiority without a matching comparison. For optimization, follow [Decide's model scope](decide.md#optimization-framing-and-method-selection): name the objective, hard constraints, candidate restrictions and what optimality is or is not established.

### Data flow, responsibilities and state

Trace one accessible input record or user action through validation, transformation/decision, persistence and final output. Name the actual files/functions and intermediate fields, not only framework names. Explain grouping keys, units, identifiers/relationships and what state is reset, shared or isolated between processing groups when relevant. For a web service connect the event, request, server rule, transaction, response and visible result, including permission checks. State which paths use a full page or partial update according to code. For a batch/report task explain its real pipeline without inventing screens or storage. Include how changed inputs reach a regenerated result and how stale output is recognized.

### Implemented scope and reproducible verification

Map mandatory behavior and major claims to implementation, actual checks and remaining gaps. Distinguish working and exercised, implemented but untested, demo/mock, assumption, and unimplemented. Expose missing mandatory work rather than labeling the whole result complete. Give the real working directory, environment/dependencies, inputs/settings, runnable commands and expected observable outcomes needed by another person to reproduce the checks. Mark commands not run here as suggested; do not invent file paths or expected counts. State what a check cannot establish, including browser behavior or live integration. Follow [Verify](verify.md) for new checks; explanations do not grant deployment, submission or product-change authority.

### Normal, boundary and failure behavior

Walk one normal case and the consequential failure paths supported by the code: relevant missing/duplicate/invalid input, permission denial, unavailable resources, no feasible result, interrupted search or transaction failure. Select applicable cases instead of imposing a universal checklist. For each explain the trigger, detecting component, returned error/status, saved or rolled-back state and recovery path. Separate observed checks from branches only inspected and cases not handled. Never teach a desirable fallback as if it were implemented. If a time-limited search exists, distinguish a retained checked result from a failed run and an unresolved search from proven infeasibility.

### Result claims, limits and independent evidence

For any claimed improvement or aggregate, trace source population/period, inclusion/exclusion rules, units, numerator/denominator and calculation to the output. Compare baseline and changed method on matching inputs and constraints; explain absolute versus relative change when relevant. Check whether missing groups, sampling, changed assumptions, resource costs or adverse effects alter the conclusion. A correct calculation on sample data is not proof of real-world benefit or causation.

Name evidence independent of the producing logic: an expectation derived from source rules, a separate recomputation from raw records, a small hand-checkable case, or appropriate observed operating data. Repeating an AI claim or re-reading the same computed score is not independent validation. Separate checks already performed from proposed sensitivity tests, measurements or trials and the conclusion each would support. If the result has no numerical improvement claim, discuss its actual correctness/operating limits; do not manufacture a percentage, baseline or study. Finish with the most consequential remaining limit and a concrete next check, not an invented score.

## Teach first; rehearse when requested

By default deliver the explanation before asking the user to demonstrate understanding. For an explicit quiz-first request, honor that mode. A request to explain does not authorize an extended interview, new implementation or an automatic question loop.

When practice is requested, select questions from consequential choices and evidence gaps in the current result. Ask one question, wait for the user's own explanation, then compare it with the inspected artifacts: what matches, what is missing/incorrect, supporting evidence and a focused clarification. A useful follow-up changes one assumption or boundary and asks how the outcome changes. Do not show a model answer before a quiz-first response, invent grading weights, promise exam coverage or declare mastery without observing the user's explanation. Preserve only useful unresolved understanding gaps in existing DECISIONS if resumption needs them.

Apply [competition restrictions](profiles.md#competition-restrictions): teaching and rehearsal occur only while AI assistance is permitted. Once the AI-prohibited assessment phase begins, do not answer, draft, rewrite or coach those live assessment responses. The permitted preparation feature is not an exam-answer mode.

For recurring deliverables retain the [operational handoff](handoff.md) in existing documentation: actual owner/environment/trigger, latest-result identification and unknowns. Use the task's required submission format when documentation is required; otherwise the conversation is enough.

**Exit:** The explanation links consequential claims to current artifacts, enables reproduction of the stated checks and exposes missing/untested behavior and decision costs. Delivering the explanation is not proof of the user's understanding; practice is complete only to the extent observed in their replies.
**Fallback:** If explanation exposes a contradiction, inspect the smallest relevant code/input/output case and mark unresolved claims. Fix only within already authorized scope, then refresh affected evidence and explanation. Do not fill a gap with a confident story or silently add a feature.
