# Validation — v0.5 / 2026-11-02

## Current v0.5 checks

Windows / Python 3.13, no added kit runtime dependencies:

- `python -m unittest discover -s tests -q`: 81 passed, 1 skipped, 0 failed. Five new behavior tests cover core installation, additive full installation preserving every existing file and evidence, core-to-core installation and missing-full-assets rejection, preservation of custom optional code, and rejecting a changed goal before copying optional files. Existing failure, dependency, stale-evidence and recipe integration tests also passed.
- `python -m unittest discover -s examples/request-priority -q`: 6 passed. Total distinct automated cases: **87 passed, 1 skipped, 0 failed**. The skipped test requires symlink creation unavailable on this host; the Windows junction test ran.
- Same synthetic request-queue demo on v0.4 and v0.5: identical result bytes. Default installed skill files decreased from **35 to 19** (excluding Python caches); full installation still contains 35. AGENTS.md and generated task records are separate and unchanged in count. Both versions already use add → verify --handoff; this version does not further reduce the two bookkeeping calls.
- The installed core CLI ran an actual acceptance checker, detected a changed delivered result, recorded the failed check in handoff, then recovered after restoring the result while preserving the failure log. Adding full assets afterward left existing records byte-for-byte unchanged.
- The new CLI read verified v0.4 schema-1 evidence without changing the old records. Competition restrictions and rubric instructions remain byte-identical to v0.4.
- Skill-creator `quick_validate.py` passed for the full and installed core skill. Local Markdown file links resolved: 44 in the final repository, 25 in the core skill. All 21 Python source files parsed using Python 3.10 grammar; this is not a Python 3.10 runtime test.

The source-first workflow, interview stopping rules and mandatory-versus-optional implementation guidance were reviewed for consistency across SKILL, START, modules and prompts. No fresh-agent behavior trial or real contest task was run for this release. Fewer installed files do not demonstrate shorter development time, better problem definition, higher scores or 80% domain coverage. Native Linux and the contest server remain untested.

The sections below are historical evidence, not additional v0.5 test runs.

## Historical v0.4 checks — 2026-10-30

Windows / Python 3.13, with no added runtime dependencies:

- `python -m unittest discover -s tests -p test_fde.py -v`: 30 passed. Seven added tests exercise direct verification plus handoff, failed retries replacing a green snapshot, timeouts and input mutation, user-owned handoff preservation before execution, active ownership/dependency guards, progress-versus-requirement changes, and the installed semantic-negative example (also under `python -O`).
- `python -m unittest discover -s tests -p 'test_recipe*.py' -v`: 46 passed, 1 skipped. All three existing execution recipes and installed lifecycle are retained. The host still cannot create the symlink used by one test; the Windows junction test ran and passed.
- `python -m unittest discover -s examples/request-priority -v`: 6 passed.
- `python demo_negative_check.py`: accepted the agreed example and rejected a plausible wrong result with unchanged row count and IDs; original example bytes were preserved.
- Skill-creator `quick_validate.py` in UTF-8 mode: valid.

Total distinct automated test cases: **82 passed, 1 skipped, 0 failed**. No new independent-agent evaluation is claimed for this version. The short lifecycle is exercised by the existing real demo integration test, which also damages the delivered result and confirms rejection.

The reduction is in bookkeeping: after initialization, single-owner `add → verify --handoff` replaces separate add/start/ready/verify/handoff calls. Implementation, meaningful check construction and reading the results are still required. There is no measured claim of overall time savings or domain coverage. BRIEF hashing, dependencies, evidence freshness, competition restrictions and schema 1 remain in place.

The sections below are historical validation of earlier versions, not additional v0.4 runs.

## Historical v0.3 / 2026-10-30

## Current change

Windows, Python 3.13.5: the initial `python -m unittest discover -s tests -v` run discovered 68 tests: 67 passed, 1 skipped, no failures. After two additional GitHub review findings were fixed, `python -m unittest discover -s tests -p 'test_recipe*.py' -v` ran 47 tests: 46 passed, 1 skipped. Combined current coverage: 23 existing CLI regressions, 46 recipe tests and 1 installed lifecycle test. The skipped test could not create a symlink under this host's permissions; a real Windows junction escape test passed.

The installed lifecycle ran all three recipes in a Unicode/spaced project path, checked known business outputs independently, recorded verified tasks and generated handoff. It also rejected changed inputs, output bytes, recipe code and an added document. [AUDIT.md](AUDIT.md) details findings, fixes and limits. Tests were authored/executed in this implementation session. The repository's separate GitHub Codex review reported grouping-key collisions and silently skipped unreadable directories; both were reproduced and fixed with regression checks. No post-fix approval by that reviewer is claimed.

Additional current checks: original request-priority example 6/6 passed; official skill-creator quick_validate passed with Python UTF-8 mode; all local Markdown file links resolved; all Python source parsed using Python 3.10 grammar. This syntax check is not execution on a Python 3.10 runtime. Total distinct current test cases across both suites: 75 passed, 1 skipped.

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
