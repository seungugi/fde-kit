# Problem brief and implementation specification

Keep current requirements consistent with the goal in state.json. Brief edits invalidate earlier verification; progress and rationale belong in DECISIONS.md.

## Goal, deliverables and constraints

State the user/job and input → processing → usable result. List each mandatory deliverable with its requirement ID, source/section, path/format and completion condition. Reference existing documents instead of copying them. Include environment, deadline, submission and prohibited actions. Distinguish optional improvements. Do not invent evaluation weights.

## Evidence and operating context

- Observed data: file and row/key or calculation; structure, representative cases, missing/duplicate values and relevant units/time zones.
- Coverage limits: represented periods/groups/channels; missing situations or unrecorded events. Absence from the sample is not zero demand or absence of a problem.
- Reported context: stakeholder statement, source/answer ID and authority if established. Keep this distinct from measurement and from the participant's choices.

## Implementation specification

Use one compact block per requirement/decision, or an equivalent table in the prescribed document. Write a draft before the first question and revise it as answers arrive.

- ID/source and required result: requirement ID, original source and input/output behavior.
- Evidence → implication: data finding or stakeholder report and its locator; how it affects the proposed implementation. State when no relevant evidence is available or needed.
- Options and tradeoffs: viable alternatives with benefit/cost and recommendation, or a link to their DECISIONS entry. A rule prescribed in the task is already specified, not a new user choice.
- Status/question: specified / pending / confirmed / delegated; answer source or question ID, intended respondent (participant or stakeholder), blocked work and explicit delegation boundary.
- Current rule and acceptance: confirmed behavior and concrete expected cases. Keep unresolved rules and their expectations pending; update both when the answer changes.

## Next unresolved question

Identify the next single question and its linked specification IDs. Other unresolved items may remain listed but unasked. Use neutral fact questions for the stakeholder and alternatives with tradeoffs for participant choices. Record the actual answer/history in DECISIONS and update affected requirements here. Result-neutral internal implementation is delegated by default.

For a small task, these connections can be a few completed bullets. Reuse this document instead of adding separate interview, analysis or plan files. Before implementation, check that the next work unit's mandatory requirements and relevant details are specified, confirmed or delegated and that acceptance matches them.
