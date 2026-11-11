# Implementation plan for `shopify-analytics`

## P0: Merge the two knowledge packages — published

- Preserve the original `AGENTS.md` as the durable analytics and instrumentation contract.
- Add navigation and methods under `docs/`; structured historical facts and decisions under `records/`.
- Include the reconstructed former-private business history with explicit operator authorization.
- Scan published content for credentials, secrets, customer PII, raw checkout URLs, and source code with embedded credentials. Account IDs, costs and campaign IDs are intentional business-history disclosures, not secrets.
- Correct former `PRIVATE` documentation labels while preserving provenance and keeping `state/constraints.yaml` explicitly historical.

## P1: Better evidence and state models

- Append future `insights/`, `decisions/`, `experiments/`, `runs/YYYY-MM/*.jsonl` and verification references with scope and status fields.
- Do not put raw source responses with customer data, credentials, private access URLs or full checkout token parameters into the public repository. Redact by allowlist or keep such source files in an access-controlled evidence store.
- Link historical reconstructed operations to actual Google Ads / Shopify change-history exports, snapshots and SHA-256 digests as independently available. Do not invent missing historical timestamps.
- Current-state business constraints require TTL, scope, actor authority and revalidation; no static file grants permission to change ad budgets.

## P2: Validation and automation

- Validate JSON/YAML schema, nonempty IDs, lifecycle statuses and supersession chains, unique operation IDs, currency units and micros scaling.
- Detect missing provenance, stale status observations, malformed evidence references, duplicated action IDs and accidental sensitive content before public commit.
- Create a generated index for methods, insights, decisions, runs and experiments.
- Create an importer from approved connector/API responses to minimal allowlisted `observation.json` and `action.jsonl` records; never automatically publish tool arguments or raw responses.
- Every Agent mutation needs scoped approval, before-snapshot, readback, rollback check and concurrent-resource ownership.

## P3: Ongoing growth operations

- Weekly review observations for promotion to stronger insights or repeatable methods; keep evidence and counterexamples.
- Separate own-stock profit objective from sourced-catalog market-information budget.
- For each experiment, preregister objective, offer, channel, test budget, maximum planned subsidy, data quality limits and stop conditions.
- Compare Google Ads clicks with Shopify/GA4 sessions and verified non-test orders without forcing metric equality.
- Model promo and non-promo economics separately, with country-local dates and currency conversion provenance.

**Publishing rule:** Reconstructed business records have been approved for this public release. Future sensitive raw evidence still requires content-level review before public commit.
