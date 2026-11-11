# Supermetrics plugin methodologies — distinguish workflows from account-specific findings

**Source provenance:** Installed Supermetrics skills `marketing-data-queries`, `ecommerce-roas-analysis`, `funnel-and-tracking-audit`, `wasted-spend-audit`, `budget-pacing-allocation`, `campaign-performance-review`, `ad-creative-performance`, and `campaign-management`. These are methodological capabilities, NOT by themselves proof of MaxSensual performance.

## 1. Query discipline (most frequently used in this case)

`data_source_discovery` → `accounts_discovery` → `field_discovery` → `data_query` → if asynchronous `get_async_query_results` → inspect `success`, `cache_used`, `cache_time`, `requested_field_ids`, `notes`, row count, source account and timezone → calculate → interpret.

Keep report type consistent. Ad account currencies differ from Shopify settlement currency. Use explicit date ranges and source-account timezone; distinguish partial days and cached data. For account changes, query exact campaign and child asset resource IDs; before/after readback is mandatory.

## 2. Marketing workstreams provided by plugin

| Plugin workstream | Workflow | Preconditions | MaxSensual applicability |
|---|---|---|---|
| Ecommerce ROAS | Daily spend + purchase value, blended ROAS, day-of-week | Trustworthy non-test purchases, consistent currency, comparable attribution | Not yet a winner/loser evaluation without real orders |
| Product/SKU attribution | Join backend sales with ad product data, score ROAS × margin × units | SKU identity bridge and actual attribution | GA4 title changes need item ID consolidation; no automatic inferred SKU-sales join |
| Promotion anomaly | Daily ad set cost/order vs prior 6 days; flag >3× | Stable baseline and functioning purchase events | Early campaign data insufficient; promo discount affects unit economics |
| Customer mix | New vs returning buyer sales and CAC | Order-level buyer status, not GA4 first session | Wait for actual buyer base |
| Basket/AOV | Order value percentiles, items/order, threshold proximity | Actual orders and discount/shipping checkout | G2PAR2 failure was stacking rule, not proof that bundles have no demand |
| Funnel audit | Ad clicks vs GA4 sessions vs Shopify purchases | Comparable source/time/model and identity linkage | Useful for distinguishing instrumentation gap from checkout blockage |
| Search waste | Query × ad group × SKU → evaluate relevance and cost → scoped negatives | Actual search terms, link to landing SKU | Egg query landing on non-egg product; ad-group exact negative |
| Budget pacing | Cumulative spend vs period target; track off-pace ±15% default | Completed comparable days and actual budget type | Under-spent budget ≠ need to increase budget |
| Campaign review | Yesterday vs trailing 7-day baseline; WoW deltas | Sufficient history; day comparable | Two partial days cannot establish trend |
| Creative fatigue | Frequency vs CTR decline vs spend | At least meaningful impressions; cross-day frequency not addable | Not usable on 30 Search impressions |
| Creative tests | Winner by CPA/ROAS, format and hook | Sufficient conversions and controlled creatives | Do not redesign RSA on 3 clicks |
| Campaign management | Read → approvals → write paused → partial failures → readback | Per-campaign explicit authorization | Applies to AG-B, G2X, CPC micros and promo gates |

**Default plugin diagnostic thresholds are examples, not universal laws:** previous 7 days for daily baseline; >25% click/session discrepancies can prompt a tracking audit; 3x promo CPA spike vs prior 6 days; ±15% pacing deviation; ~10 conversions / ~1,000 impressions to avoid making optimization decisions on noise. Small campaigns with fewer observations should be labelled INSUFFICIENT rather than “good” or “bad.”

## 3. Account-specific insights observed from this practice

- An adult-wellness Search ad may be `APPROVED_LIMITED` under `NON_FAMILY_SAFE` and still deliver some impressions. `LIMITED` is NOT `DISAPPROVED`.
- `isExemptible=true` on a violation means a legitimate request path exists. Successfully adding a keyword via exemption does **not** prove the RSA is approved or the campaign is eligible to serve.
- A low CPC and unusually high CTR in a mature campaign is an investigation signal, not independent proof of bad traffic, bots, or residual inventory.
- Phrase/exact keywords cover close variants; that can reveal demand (queries) but also accidentally map to an incompatible product form.
- A merchant's 30% automatic discount can supersede a non-combinable BXGY code; valid coupon configuration does not guarantee it can be used in the cart.
- Product analytics grouped by title will fragment when a title changes; use immutable item/product IDs before aggregating.
- GA4 `purchase` from an owner payment test proves collection of an event, not real-customer revenue attribution.
- `write_status=applied` plus normalized connector status is not enough where it contradicts exact raw platform network flags; log both and reconcile by field definition.
- Copying an account amount into Google Ads micros is a high-impact risk; use unit conversion tests and actual post-write readback.

## 4. Insight qualification template

For each claim: observation window, scope, unit, value, source tool, source freshness, affected products, evidence URIs, data contamination, alternative explanations, decision that used it, follow-up result, confidence, expiry/review date. The operator authorized publishing selected account-specific historical figures in `records/`. Do not publish customer PII, credentials or unreviewed raw API payloads; record freshness, uncertainty and source for every numeric claim.
