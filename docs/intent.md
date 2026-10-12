# Intent

Create an extensible public security pipeline collection for KaizenxRyu. Begin with a repeatable agent security boundary demonstration, and provide a researched route to Microsoft's ASSERT evaluation workflow. This is independent work, not a Microsoft product or endorsement.

Acceptance for the first local revision:

- Known forbidden tool calls are rejected and legitimate calls remain allowed.
- Baseline and governed variants use identical case IDs and suite fingerprints.
- Schema errors and missing reports fail; overrefusal fails.
- Reports disclose synthetic execution and zero model calls.
- Each run produces ten assessment documents, a printable visual overview and an evidence manifest. They retain the same run fingerprint, hash their source report and files, and keep production readiness and human sign-off pending. Live-model and company-specific requirements cannot be marked passed.
- Source is modular, has no runtime dependencies or credentials, and workflows have immutable action pins.
- ASSERT documentation uses actual upstream interfaces and clearly separates unexecuted integration from the tested demo.
- Public publication and hosted Actions execution are separately verified, never inferred from local checks.

No cloud resources, subscription API spend, production scanning or changes to Kaizen's backend are part of this initial local build.
