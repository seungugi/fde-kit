# Environment profiles

Profiles are agent guidance, not a network firewall, environment configuration or competition approval. The user's current rules and supplied task take precedence.

| Item | standard | competition |
|---|---|---|
| Memory | Project-local brief, state, evidence, handoff | Same; no external memory connection |
| External services | Only as authorized for the task | Provided environment/tools and allowed public inbound resources only |
| Credentials | Existing authorized access only; no automatic account connection | No personal API keys/subscriptions |
| AI model | As authorized in the current environment | Provided Codex only; follow the event's Astra restriction |
| Computer Use | Only if available and authorized for the task | Prohibited at every stage; no automated screen interaction |
| Delegation | When available and authorized, bounded by contracts | Same, within provided tools and time/token constraints |
| Completion | Acceptance, current evidence, handoff | Required deliverables, current evidence, submission buffer, own understanding |

## Competition restrictions

These restrictions apply to `competition`, not to ordinary `standard` projects. They reflect the SK hynix event guides reviewed 2026-10-30: the essential-checks brief, "제한 사항" and "추가 안내사항"; and the detailed environment guide, sections 8 and 9. Follow the actual event rules and any updated official notice.

- **Computer Use (automated screen interaction) is prohibited at every stage.** Do not use computer-use tools to click, type into or otherwise operate the exam UI, browser or messenger. Do not replace a prohibited interaction with another automation tool or route. The participant operates those screens. Terminal-based code execution and tests remain available within the event's permitted scope; this is not a ban on ordinary coding commands.
- **Astra usage is restricted for this event: do not select or use Astra.** Use only the Codex and permitted models provided in the exam environment. The guide recommends Sol 6.1, Terra 5.6, Luna 6 and Sol 6.0; these recommendations do not establish availability in a particular session. At the start or resumption of competition work, check the current model using the provided controls when available; do not claim a check you cannot perform. If Astra is selected, have the participant choose a permitted model through the platform's supported controls before continuing AI work. Do not modify credentials, platform-managed configuration or connection processes to change models or bypass a restriction.
- Obtain allowed public skills, GitHub tools and reference material through the AI inside the provided environment. Do not directly browse external sites outside that environment or upload private PC files. Public download permission does not permit bringing in an externally generated complete answer.
- Keep problems, files, artifacts and work records inside the provided environment. Do not Git Push, connect an external AI or memory service, or supply personal API keys/subscriptions. A permitted tool must still comply with these restrictions.
- Do not use AI during the follow-up written-answer phase, including via another browser or device. Finish any AI-assisted explanation practice during the permitted task phase; the participant writes the follow-up answers independently.

The CLI does not enforce model selection, screen-use restrictions or network isolation. These are instructions for using the kit within the event's actual controls. If a permitted operation is blocked, use the platform's issue-reporting route rather than bypassing the restriction.

Suggested 180-minute practice budget: 15 minutes framing, 15 end-to-end spike, 80 implementation/checks, 35 integrated validation, 20 explanation/documentation, 15 submission buffer. Shorten this to respect any earlier overall deadline. Installation should not consume the task; if an optional framework cannot be made ready promptly, continue with the self-contained kit.

Do not modify platform-managed configuration or connection processes, start unapproved memory services, export evidence to issue trackers, or automatically publish this kit. Keep raw verification logs local and inspect them before any authorized sharing.
