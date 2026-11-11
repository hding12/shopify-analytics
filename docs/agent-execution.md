# Operational discipline for agents, plugins and automation

## Standard execution state machine

`OBSERVE → NORMALIZE → HYPOTHESIZE → PROPOSE → APPROVAL_GATE → EXECUTE → READBACK → EVALUATE → ARCHIVE`

A `PROPOSED` change is never recorded as `EXECUTED`; tool success never automatically becomes `READBACK_VERIFIED`.

Before each write:
- Load stable instructions and current scope-specific constraints.
- Read the platform resource and snapshot the original state.
- Determine whether action affects real spend, customer-facing claims, discounts, product data, pixels, analytics/privacy or inventory.
- Match against explicit permissions, campaign IDs, spend type/currency, approved fields and stop conditions.
- If another agent or scheduled script touches the same resource, acquire a lock or arbitrate. Never silently overwrite.

After each write:
- Capture API result, partial failures and notes; fetch again using the same source of truth (and raw API when needed).
- Compare actual changed fields to allowlist; verify no collateral changes. Verify frontend where needed (PDP mobile, checkout cart, live ad review).
- Write append-only event with source URI/hash, actor, authorization, before/after, verification, rollback plan and next follow-up.

## Four permission tiers

1. `READ_ONLY`: live queries, reporting, snapshots.
2. `DRAFT_ONLY`: proposals or paused campaigns; no spend or user-facing publishing.
3. `WRITE_APPROVED`: product, discount, ad and targeting edits with exact allowlist.
4. `SPEND_APPROVED`: enabling/raising spend, with account/campaign budget and stop gate.

A broad “continue” message is not approval to expand target resources; previously granted scope and approval gates persist until replaced.

## Incident anti-patterns

- Google Ads budget account currency and microscopic units; validate `human_amount × 1,000,000` before write and do not silently scale by 100×.
- A positive keyword creation result is not RSA approval; campaign PAUSED can mask other eligibility issues.
- Native API and normalized connector flags can disagree; retain raw field names and actual values.
- HTML regex boundary deletion can remove unrelated content; use parser + semantic invariants + diff before publishing.
- Checkout auto discount and shipping discount may be noncombinable. No shipping promise until address-aware checkout verifies.
- A recommendation cron/`run_daily` can override manually changed collection sort; coordinate writes.
- New campaign should be PAUSED; never conflate approval to create with approval to activate.
- Plugin data queries may return cached rows. Store `cache_time` and rerun fresh after writes when supported.

## Evidence storage

The operator approved public release of the reconstructed business-history records, including merchant-source prices, ad account IDs and budgets. **Do not** publish raw snapshots containing customer data, receipts with personally identifying fields, live tokens, passwords, full checkout URLs, or unreviewed provider payloads. Store such raw evidence in access-controlled storage, and publish safe hashes/pointers where useful. Credentials never belong in logs, public or private.
