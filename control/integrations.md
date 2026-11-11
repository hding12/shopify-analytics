# Integration contract — Growth control (v1)

The **public** `hding12/shopify-analytics` repository is the *decision index*, not the production configuration service. The **private** `hding12/maxsensual-recs` repository is a separately owned implementation. Do not merge, modify or dispatch jobs to it as part of this patch.

## Sources of truth

| Question | Authority |
|---|---|
| What does the business want / what has approval? | Approved decision + `control/experiments.json` and scoped chat authorization |
| Is an ad enabled / which goals are actually active? | Google Ads raw API and post-change readback |
| Are recommendations published? | Shopify collection readback, publication marker and private execution journal |
| Is the campaign successful? | Independent non-test Shopify order validation and contribution profit, not GA4 carts |
| Is a dry run safe? | Recommendation engine's own read-only tests; no `apply` |

## Read-only coordination in this phase

1. At the beginning of a growth decision, run `python3 scripts/growth_control.py status` and consult the latest platform state. The JSON snapshot is not automatically refreshed.
2. For a proposed change, run `python3 scripts/growth_control.py check-change --resource shopify:collection:para-ella` or another concrete resource. `APPROVAL_REQUIRED` means human review, **not** an API-level lock.
3. If a change is approved in the future, create a scoped change plan with preflight, rollback, permissions, cross-experiment impact, and new attribution boundary, using existing `docs/agent-execution.md`.
4. After an action, return a *sanitized* execution summary to the market repo. Production systems remain authoritative; no raw customer details or secrets belong in public Git.
5. The recommendation repository is read-only for now. Its `publishing_enabled` and Actions flags stay untouched. Do not silently convert this document into approval to publish.

## State versus enforcement

- `control/experiments.json` records a **manual decision gate**. It does not automatically block GitHub workflows or Shopify API writes.
- The `check-change` command is local advisory preflight only. No background service, synchronization, or remote lock is installed.
- A historical observation may be stale; require fresh source readback immediately before any production write.
- Do not reuse the old T08 add-to-cart pixel patch. Its duplicate-event assumption was invalidated by production evidence and the patch was rolled back.

## Future integration (not implemented or authorized now)

When the user decides to connect the recommendation execution pipeline, use a **read-only** fetch of a versioned market policy and a mandatory fail-closed publication gate. Pin the market policy commit SHA, log the approved decision ID, lock resource ownership, and read back Shopify changes. Never use the market repository's public status files as credentials or blanket production authorization.
