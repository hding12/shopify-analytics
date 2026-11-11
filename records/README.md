# Published G1/G2/G2X historical records

**Publication:** The operator expressly authorized releasing these historical business records to the public `hding12/shopify-analytics` repository on 2026-11-11. This folder was originally prepared as a private companion bundle; its designation has been superseded by this public release.

These records reconstruct events from operator/Agent reports and selected independently verified connector readings. They are **not** a complete audit trail and **do not** contain the original API request/response snapshots, screenshots, purchase logs or evidence hashes.

Contents include product IDs, Campaign and Ad Group IDs, ad budgets, estimated sourcing costs and references to an operator test payment. The package contains no intentionally included customer names, email addresses, passwords, access tokens or raw Checkout Tokens.

Evidence handling:

- Keep source type, date window, confidence, and evidence pointer on every claim.
- `occurred_at: null` means the actual event timestamp is not known; do not synthesize a precise timestamp.
- `EXECUTED` and `READBACK_VERIFIED` are different states; do not promote a report into independent verification.
- Replace unresolved evidence references with verified snapshots and SHA-256 hashes when they are available, but redact sensitive details before public commits.
- Treat all `state/constraints.yaml` fields as **historical**, not permissions that authorize a new write. Confirm live campaign state and current user authorization first.

See [`../AGENTS.md`](../AGENTS.md) for enduring data definitions and [`../docs/architecture.md`](../docs/architecture.md) for the record lifecycle.
