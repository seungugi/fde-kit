# Problem brief and implementation specification

One current specification, progressively completed. Keep it consistent with the goal in state.json. Changes invalidate prior verification; progress, alternatives and answer history belong in DECISIONS. Reference the original task instead of copying it.

## Goal, scope and evidence

State who needs what result and why, mandatory deliverables/paths/formats, exclusions, environment/deadline/submission constraints and sources. Do not invent rubric weights. Record decisive input findings with file/row/key or calculation and coverage limits; separate measured observations from stakeholder reports and participant choices.

## Business terms and service flow

Define only terms whose ambiguity affects behavior. Trace actor → action → validation/rule → stored or computed result → visible outcome, with required states, permissions and failure paths. Identify data entities/relationships and required screens/reports/interfaces; omit irrelevant components. Unknown operating facts remain gaps.

## Requirements and acceptance

Use stable IDs and a compact block or table per requirement:

| ID / source | Current behavior / decisive evidence | Status / question or answer ID | Concrete expected outcomes | Slice |
|---|---|---|---|---|

Status is specified, pending, confirmed or delegated. Link questions to the intended respondent and blocked behavior. Define normal and material boundary/failure cases from confirmed rules; do not invent expectations. Keep options/reasons in DECISIONS and link them. Routine presentation choices need no record.

For required optimization only, extend the same entries with decision variables/domains, objective/units/priority, hard constraints, measured scale and transformations, selected method/baseline, stopping budget and independent acceptance. Search progress/results belong in DECISIONS.

## Implementation slices

One row per independently demonstrable behavior, not per technical layer. Include only components the requirement needs. Existing CLI task IDs are enough; do not create a second ticket system.

| Task ID / requirement IDs | Actor action → visible result | UI / interface / data touched | Blocked by | Check boundary / expected cases |
|---|---|---|---|---|

For tracked slices, register exact watched files and dependencies using the existing CLI. Keep changing task status in state.json rather than duplicating it here. Link existing code/test paths when known; do not pre-create speculative files.

## Readiness and remaining gaps

Check every mandatory requirement has behavior, an implementation slice and acceptance, and each feature has a source/choice/delegation. Distinguish a ready slice from a ready whole plan. Name pending questions, respondents, affected IDs and missing inputs. Plan readiness is not verified implementation. A planning-only request ends here; authorized implementation proceeds on ready slices without another approval ceremony.

Small tasks may use a few bullets with these connections instead of filling every section.
