# Explain / AI 산출물 이해·인수인계

**Start:** A user must operate, maintain, submit or personally explain the result.
**Inputs:** Actual delivered artifacts, original requirements, decisions and current evidence.
**Output:** The required project documentation, using [explanation outline](../assets/EXPLAIN.md) only where helpful.

Trace one real input through the transformation/decision/storage/output path. Name concrete files or components. Explain the consequential design choice, a plausible alternative, why it was not selected, what was checked and what would break under changed assumptions. Keep startup steps executable from the recipient's environment.

Use the existing README or the delivery response for a small task. For recurring outputs, follow the operational note in [handoff](handoff.md): a generation command working on the developer's machine does not establish that the recipient can keep the result current.

Do not ask the user to memorize model-authored prose. Before a competition submission, let them explain the flow and a boundary case in their own words. Correct misunderstandings while AI use is still permitted. Once the AI-prohibited written phase begins, do not answer, draft or rewrite those examination responses.

**Exit:** Deliverables satisfy required paths/formats, the user can find and reproduce the checks, and known limits are explicit. The user can explain the important choices.
**Fallback:** If explanation exposes a gap, inspect the implementation and the smallest relevant example. Do not cover uncertainty with confident documentation or new features.
