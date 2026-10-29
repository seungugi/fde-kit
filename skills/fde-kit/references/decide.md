# Decide / 해결 방향

**Start:** Need to choose scope, implementation approach, dependencies or a technical compromise.
**Inputs:** Current brief, existing assets, working environment and remaining time.
**Output:** A concise decision in `fde-notes/DECISIONS.md`: source, choice, reason, tradeoff and when to revisit it.

Inspect what already works. Prefer an existing project capability, then a standard/platform feature, then an installed dependency, then small new code. Add a new tool only if it solves a concrete requirement well enough to justify installation, integration and debugging time.

Compare alternatives only where the choice materially matters. Respect existing architectural conventions. Do not sacrifice a required behavior or validation to make code shorter. Identify a thin end-to-end result that can work early and reveal integration risk.

**Exit:** One approach meets the mandatory conditions, the excluded scope is visible, and the riskiest assumption has a cheap check.
**Fallback:** If a dependency or approach fails within its budget, use the simplest alternative that still meets the requirements. Record reduced scope honestly; never silently redefine acceptance to make a test pass.

Ponytail may assist with reuse and minimal complete changes when installed. It is optional; do not load it or other repositories merely to repeat this decision.
