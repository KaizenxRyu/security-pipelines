"""Assessment text for the actual demo scope; broader requirements remain explicit."""


def documents(result: dict) -> list[tuple[str, str, str]]:
    governed = result["runs"]["governed"]
    failed = [row["id"] for row in governed["cases"] if not row["passed"]]
    metrics = (f"Boundary verdict: **{result['verdict']}**. {result['case_count']} paired cases. "
               f"Forbidden calls allowed: {governed['forbidden_allowed']}/{governed['forbidden_total']}. "
               f"Legitimate calls blocked: {governed['legitimate_blocked']}/{governed['legitimate_total']}.")
    flow = ("```mermaid\nflowchart LR\n  F[Untrusted proposed calls] --> V[Validate fixture contract]\n"
            "  S[Trusted demo session] --> P[Authorization boundary]\n  V --> P\n"
            "  P --> D[Allow or deny decision]\n  D --> R[Paired replay and evidence]\n"
            "  R --> H[Human review pending]\n```\n\n")
    return [
        ("01-executive-summary.md", "Executive evaluation summary",
         metrics + "\n\n" + flow + "The demonstration checks authorization decisions, not an AI model. "
         "An intentionally unrestricted baseline is compared with a scoped boundary on identical calls. "
         "No tools execute and no customer data is processed. Production readiness is **NOT ASSESSED**. "
         "A company must supply its system scope and acceptance requirements before using this as a release assessment."),
        ("02-high-level-design.md", "High level design", flow +
         "CLI → JSON contract validator → paired replay → deterministic policy → JSON, Markdown and HTML reports. "
         "The pack generator reads the same result; every document carries the same suite fingerprint. "
         "Runtime dependencies: Python standard library only. There is no LLM, remote service, database or tool dispatcher. "
         "Production integration must obtain identity from the authenticated server and enforce decisions before executing tools. "
         "The demo Session is a fixture, not sign-in or an approval mechanism."),
        ("03-system-inventory.md", "System model and tool inventory",
         "| Component | State | Evidence |\n| --- | --- | --- |\n"
         "| Local replay and policy | Executed in this run | ../report.json |\n"
         "| LLM / embeddings / training | Not used | model_used is null |\n"
         "| read_invoice | Simulated authorization only | Account-scope cases |\n"
         "| read_document | Simulated authorization only | Lexical path cases |\n"
         "| fetch_reference | Simulated authorization only | URL cases |\n"
         "| Microsoft ASSERT | Not run | docs/assert-integration.md |\n"
         "| Clarity / ACS / OPA | Not integrated | docs/assert-integration.md |\n\n"
         "For a real system, record model identifier/revision/license/provider, prompt revision, datasets, "
         "retrieval sources, connectors, permissions, owners, runtime versions and deployment regions."),
        ("04-data-flow-and-privacy.md", "Data flows and privacy",
         "```mermaid\nflowchart LR\n  A[Synthetic local JSON] --> B[Local Python memory]\n"
         "  B --> C[Result without raw tool arguments]\n  C --> D[Local assessment files]\n"
         "  D --> E[CI artifacts if hosted workflow runs]\n```\n\n"
         "Inputs contain synthetic account IDs, paths and URLs. Reports omit raw tool arguments. "
         "No provider transmission occurs. Hosted workflow artifacts are configured for seven-day retention; "
         "local output remains until its owner removes it. Deleting local files does not delete GitHub artifacts. "
         "No real-system privacy assessment has been completed. Before connecting an AI target, record data classification, "
         "lawful basis/consent where applicable, residency, access, redaction, retention and deletion evidence."),
        ("05-threat-model.md", "Threat model and trust boundaries",
         flow + "| Threat | Demo boundary | Remaining exposure |\n| --- | --- | --- |\n"
         "| Caller claims another account | Exact account match | Real authentication is absent |\n"
         "| Caller supplies actor/approval fields | Exact argument contract rejects extras | Human approval must be enforced by host |\n"
         "| Path traversal / prefix confusion | Lexical path checks | Symlinks, junctions and races not tested |\n"
         "| Destination or port spoofing | HTTPS, exact host and port checks | Redirects, DNS rebinding and real egress not tested |\n"
         "| Unknown write or shell tool | Tool allowlist | Host dispatcher not integrated |\n"
         "| Indirect prompt injection | Not tested | Requires a real model and adversarial retrieved content |\n"),
        ("06-evaluation-plan-and-results.md", "Evaluation plan and results",
         metrics + "\n\nAll registered cases run against baseline and governed variants with the same fixture hash. "
         "A governed expectation mismatch fails, including blocking a legitimate request. "
         "Malformed suites fail before a report is generated. These are deterministic fixture counts; "
         "there are no confidence intervals, model safety scores or statistical generalization claims.\n\n"
         "Failed governed case IDs: " + (", ".join(failed) or "none") + ".\n\n"
         "LLM helpfulness, hallucination, privacy leakage in answers, prompt injection, bias, robustness, "
         "accessibility, latency, load, model drift and adversarial tool chains: **NOT RUN**."),
        ("07-risk-register-and-remediation.md", "Risk register and remediation",
         "| ID | Risk | Current disposition | Next action | Owner |\n| --- | --- | --- | --- | --- |\n"
         "| R01 | Authorization example mistaken for production control | Open | Bind to actual host and verify dispatch prevention | System owner pending |\n"
         "| R02 | File or network execution escapes lexical checks | Open | Add canonical filesystem and egress tests | Security owner pending |\n"
         "| R03 | Models disclose sensitive content or follow injected instructions | Not assessed | Live paired behavioral evaluations | AI owner pending |\n"
         "| R04 | Provider credentials exposed to evaluated code | Not assessed | Trusted runner, scoped credentials and budget | CI owner pending |\n"
         "| R05 | Reports used as a compliance certificate | Open | Scope requirements and review evidence | Governance owner pending |\n\n"
         "Severity and deadlines require the actual business impact and system context; they are not guessed here. "
         "Do not close open risks merely because the offline replay passes."),
        ("08-governance-and-coverage.md", "Governance and requirements coverage",
         "| NIST AI RMF function | Supporting pack | State |\n| --- | --- | --- |\n"
         "| GOVERN | Sign-off, owners and scoped requirements | Human review pending |\n"
         "| MAP | HLD, inventory, data flows and threat model | Demo scope documented |\n"
         "| MEASURE | Paired results and evidence fingerprint | Offline boundary checks only |\n"
         "| MANAGE | Risks, remediation and operations | Production actions pending |\n\n"
         "This is a high-level organizational mapping to the voluntary NIST AI RMF, not a conformance finding. "
         "OWASP GenAI resources inform future threat coverage; the suite is not an OWASP coverage certification. "
         "Company-specific requirements, sector rules and jurisdiction are **UNKNOWN**. "
         "Sources: [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) and "
         "[OWASP GenAI](https://genai.owasp.org/)."),
        ("09-operations-and-incident-plan.md", "Operations and incident response",
         "```mermaid\nflowchart LR\n  A[Failed check or incident] --> B[Stop promotion]\n"
         "  B --> C[Preserve restricted evidence]\n  C --> D[Investigate and fix]\n"
         "  D --> E[Rerun same suite and review]\n```\n\n"
         "The CLI exits 0 for offline PASS, 1 for expectation FAIL and 2 for input/output errors. "
         "Use a fresh output directory per run and check the process exit before opening results. "
         "An older PASS file is not evidence for a new failed invocation. Restore by checking out a verified commit "
         "and rerunning the suite. Keep evidence hashes with a restricted backup. No hosted runtime was deployed. "
         "A production owner must add incident contacts, detection, containment, credential rotation, recovery targets "
         "and a tested response exercise; these are pending."),
        ("10-review-and-release-decision.md", "Review and release decision",
         "| Decision field | State |\n| --- | --- |\n"
         "| Evaluation outcome | " + result["verdict"] + " for offline fixtures only |\n"
         "| Production approval | NOT ASSESSED |\n| Reviewer identity | PENDING |\n"
         "| Review date and signed revision | PENDING |\n| Risk acceptances, reasons and expiry | PENDING |\n"
         "| Applicable company requirements | UNKNOWN |\n| Re-evaluation trigger | Any policy, model, prompt, tool, data or scope change |\n\n"
         "Human reviewers must validate the evidence, ownership and remaining risks. The pipeline cannot approve itself "
         "or represent generated text as a signed decision.")
    ]
