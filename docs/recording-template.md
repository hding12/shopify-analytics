# Copyable record templates

## Method card

```yaml
id: METH-SEARCH-TERM-RELEVANCE
version: 1
scope: paid_search
trigger: "A search term buys clicks but differs from target product form"
requires: ["search-term report", "target SKU verified specification", "ad group"]
method: "Join query → triggering keyword → ad group → landing SKU → product-form intent; only then propose scoped negative"
not_sufficient: ["one click to prove conversion", "generic CTR to infer traffic quality"]
authorization: "ad group negative keyword write"
verification: "readback exact negative and ad-group scope"
source: "adapted from Supermetrics wasted-spend audit + field case"
```

## Constraint (historical record or current scoped control)

```yaml
id: CST-ADS-001
scope: {account: "private-reference", campaign: "private-reference"}
rule: "never enable unless ad policy review approved/approved_limited and campaign budget exact"
status: active
valid_from: "2026-11-11"
valid_until: null
reason: "user-approved spend gate"
source_ref: "decision:<id>"
```

## Insight (JSON)

```json
{
  "id": "INS-EXAMPLE-001",
  "title": "Close-variant query/product-form mismatch",
  "status": "OBSERVED",
  "observed_at": "2026-11-11T00:00:00Z",
  "time_window": {"start":"2026-11-10","end":"2026-11-11","timezone":"America/Santiago"},
  "statement": "A relevant adult-product term may match an incompatible form factor via a close variant.",
  "sources": ["evidence:search-term-snapshot"],
  "limitations": ["Small sample; no causal ROI inference"],
  "visibility": "internal"
}
```

## Action log (JSONL, one event per line)

```json
{"event_id":"RUN-example:0001","observed_date":"2026-11-11","occurred_at":null,"source_kind":"user_agent_report","action":"add_AdGroup_negative_exact","target":{"ad_group_ref":"private"},"authorization":"ADR-reference","execution_status":"EXECUTED","verification":{"status":"PENDING_READBACK"},"evidence_refs":[],"changed_fields":["negative_keywords"],"sensitivity":"internal"}
{"event_id":"RUN-example:0002","observed_date":"2026-11-11","occurred_at":null,"source_kind":"connector_readback","action":"verify_AdGroup_negative_exact","target":{"ad_group_ref":"private"},"authorization":"ADR-reference","execution_status":"READBACK_VERIFIED","verification":{"status":"PASS"},"evidence_refs":["evidence:readback"],"changed_fields":[],"sensitivity":"internal"}
```

Example timestamps with `00:00:00Z` in this template are placeholders and not historical event times. Never reuse them as facts.
