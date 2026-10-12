# Primary source ledger

Reviewed 2026-10-12. Upstream information is interface research, not evidence that this repository ran those integrations.

| Source | What it supports | Status here |
| --- | --- | --- |
| [Microsoft run-assert-eval article](https://commandline.microsoft.com/run-assert-eval-responsible-ai-agent-risk-discovery-at-runtime/) | Requirement-based discovery, evaluation and reviewed controls; published 2026-09-24 | Researched |
| [ASSERT at 4984800](https://github.com/responsibleai/ASSERT/tree/49848007ee2d4e208a5cf53a046f4ef164860720) | Callable targets and evaluation configuration | Not run |
| [ACS guide](https://github.com/responsibleai/ASSERT/blob/49848007ee2d4e208a5cf53a046f4ef164860720/docs/guides/securing-agents-with-acs.md) | Policy generation, validation and host integration limits | Not integrated |
| [ASSERT action at 4e22663](https://github.com/responsibleai/assert-ai-action/tree/4e22663a2b47db41712a01fb70cd66534410662e) | Existing CI regression gate; baseline/verdict behavior | Not run |
| [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | Voluntary GOVERN, MAP, MEASURE and MANAGE functions; not a universal checklist | High-level pack mapping only |
| [OWASP GenAI 2026 announcement](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/) | Updated LLM and agent security guidance available for future scope | Coverage not certified |

Direct action pins were checked against remote Git tags and official action.yml contracts: checkout v6 `d23441a48e516b6c34aea4fa41551a30e30af803`; setup-python v6 `ece7cb06caefa5fff74198d8649806c4678c61a1`; upload-artifact v6 `b7c566a772e6b6bfb58ed0dc250532a479d7789f`. They use Node 24. CI's Python patch version is pinned to 3.12.15, observed in the first successful hosted run. Review upgrades explicitly.
