# Runbook

## Local execution

From the repository root, run the tests and replay commands in README.md. Use a fresh `--out` directory per invocation. Check the exit code first, then `report.json` and `assessment/manifest.json`. The manifest identifies the report and generated documents by SHA-256. Matching hashes establish file integrity, not reviewer identity or a digital signature.

## Hosted pipeline

The credential-free GitHub Actions definition is the infrastructure for this example. It runs tests, replays the fixtures and uploads the entire report/assessment folder for seven days. Local success does not prove a GitHub run; verify its job conclusion and download the artifact after publication. Never add provider keys to this workflow.

## Failure and recovery

- Exit 1: inspect failed governed cases and legitimate blocking. Fix policy or incorrect expectations with review, then rerun.
- Exit 2 or absent reports: treat the invocation as failed. Partial files and older reports must not be promoted.
- Hosted job failure: inspect failed steps; a job summary or uploaded partial artifact is not a pass.
- Suspected evidence change: compare recorded hashes, preserve the original run and regenerate from a trusted source revision.

## Backup and rollback

Back up the source Git revision plus complete output directory and manifest to restricted storage. Test restoration by checking out the same revision, restoring the suite, rerunning and comparing its fingerprint/counts. Timestamps will differ. Roll back source with a reviewed revert or an isolated checkout of a prior verified revision; do not overwrite unrelated work. No running application or cloud resource exists to roll back.

## Release checklist

Record source revision, Python version, suite fingerprint, test output, report hashes, review disposition and public CI run URL. Confirm no secrets or private customer files are tracked. Live ASSERT requires the separate activation checklist and explicit budget approval. Production readiness requires a real system assessment, never just this demonstration's PASS.
