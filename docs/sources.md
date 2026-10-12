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

Direct action pins were checked against remote Git tags: checkout v4 `11d5960a326750d5838078e36cf38b85af677262`; setup-python v5 `a26af69be951a213d495a4c3e4e4022e16d87065`; upload-artifact v4 `ea165f8d65b6e75b540449e92b4886f43607fa02`. Review upgrades explicitly.
