# Validation — v0.3 / 2026-10-30

## Current change

Windows, Python 3.13.5: `python -m unittest discover -s tests -v` discovered 68 tests: 67 passed, 1 skipped, no failures. Includes 23 existing CLI regressions, 44 recipe tests and 1 installed lifecycle test. The skipped test could not create a symlink under this host's permissions; a real Windows junction escape test passed.

The installed lifecycle ran all three recipes in a Unicode/spaced project path, checked known business outputs independently, recorded verified tasks and generated handoff. It also rejected changed inputs, output bytes, recipe code and an added document. [AUDIT.md](AUDIT.md) details reproduced findings, fixes and limits. These checks were authored/executed in the same implementation session; they are not a fresh-agent or external audit.

Additional current checks: original request-priority example 6/6 passed; official skill-creator quick_validate passed with Python UTF-8 mode; all local Markdown file links resolved; all Python source parsed using Python 3.10 grammar. This syntax check is not execution on a Python 3.10 runtime. Total executed test cases across both suites: 73 passed, 1 skipped.

The following 2026-10-29 section is retained as historical evidence for v0.2. It does not imply the new recipe behavior received the same historical independent-agent evaluation.

## Historical validation — 2026-10-29

## Executed checks

- Python 3.12 on Windows: 23 CLI behavior tests passed. Tests cover preservation, repeat initialization, task ownership/dependencies, actual command execution, failures/timeouts, in-progress state, changed artifacts/brief/intent/evidence, dependency changes during verification, handoff freshness, rejection of corrupt delivered output, rubric provenance/coverage/re-registration, and terminal launch arguments/project directory.
- Request-priority example: 6 tests passed, including a real command-line output check. The final delivery checker also compares the actual result.json with an independently written expected sample.
- Full example lifecycle: initialize → add/start → create output → ready → verify → modify input → observe needs_verification → reverify → handoff.
- Official skill-creator quick_validate: valid. PyYAML was used in a separate validation environment only; it is not a runtime dependency of the kit.
- Actual Codex app-server skills/list: fde-kit found enabled at the project-local .agents/skills/fde-kit/SKILL.md path. This did not send a model prompt.
- Independent fresh-agent use: resumed the separate shipping exercise, corrected a boundary condition and quantity validation, generated the output and run instructions, passed 8 tests, and left verified records and handoff.
- Independent review identified dependency-race and delivered-file-check gaps. Both were reproduced by failing tests, corrected, and covered by passing regression tests. Focused re-review found no new important issue in those changes.
- User-led coaching scenario: an independent agent reviewed an approach under a 30-minute constraint, kept speculative weights separate from confirmed deliverables, identified concrete gaps, and did not implement code when the user requested review only. This is one behavior sample, not a guarantee across models.
- Version 0.2 review found that re-registering an unchanged criterion label could preserve stale evidence after source text changed. A failing CLI test reproduced it; per-criterion revisions fixed it. The regression test passed and focused re-review found no material remaining issue.

## Interpretation and limits

The baseline agent without this skill also identified the shipping logic defects. This exercise establishes that the kit can be used, not that it improves model intelligence, competition scores or reliability by a measured percentage. No scoring benchmark was performed.

Native Linux execution and the actual competition server were not available for validation. The runtime uses Python standard-library APIs and has no shell-specific setup dependency, but target-environment verification is still necessary. The kit has not been approved for competition import.

CLI evidence covers explicitly declared local files and the chosen command. It does not prove test adequacy, automatically detect undeclared/environmental changes, or enforce data/network policy. Installed skills are snapshots; this initial release deliberately refuses to overwrite a different or edited installed copy. Review updates explicitly.
