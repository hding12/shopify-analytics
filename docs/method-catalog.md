# Cross-domain method catalog

Every method card should specify: question, trigger, prerequisite evidence, input source & unit, procedure, exclusions, uncertainty threshold, decision output, authority to act, verification and escalation/stop condition.

| Code | Method | Reusable core | Real-world failure case it prevents |
|---|---|---|---|
| M-01 | Data contract before comparison | Align unit, date, currency, attribution scope, filter, sample and account | Treating Ads clicks as Shopify sessions |
| M-02 | Evidence ladder / competing explanations | OBSERVED ≠ VERIFIED ≠ CAUSAL; capture alternatives and scope | 40% CTR and cheap CPC falsely labeled bots or worthless inventory |
| M-03 | Cross-system purchase reconciliation | Native backend paid orders, test classifications, GA4 purchase, ads conversions | Platform `test=false` treated as human purchase |
| M-04 | Buyer path audit | Collection quick-add, cart permalink, PDP, checkout, payment are distinct routes | Misinterpreting no PDP view as no shopping intent |
| M-05 | Product sourcing/market probe | Interest → paid order → replication → future bulk buying | Rejecting probe SKUs solely due to dropship loss |
| M-06 | Purchase unit economics | Separate own-stock BEP_CPA from probe cost-of-learning | Incorrect CPA targets during 30% discount |
| M-07 | Search-term relevance | Match actual term to product form; use scoped negatives | Egg-form queries on a non-egg landing page |
| M-08 | Policy compliance / exemption | Read policy key and `isExemptible`; one formal review; verify ad review | Treating keyword creation as ad eligibility or synonym guessing as compliance |
| M-09 | Paid experiment design | Single primary variable, segment accounting, max risk, stop gates | Raising CPC after 3 clicks and calling it proven |
| M-10 | Discount checkout QA | Check stacking and actual checkout; timezones; display promises | Advertised code overridden by 30% automatic discount |
| M-11 | Ecommerce content regression | Before snapshot → targeted DOM edit → HTML diff → readback → mobile smoke test | Greedy section removal deleting SKU specs and shipping |
| M-12 | Safe ad campaign mutation | Read → approval → write paused → inspect partial result → readback → enable | 411 vs 4.11 micros; overwrite of other fields |
| M-13 | Multi-agent resource arbitration | Shared resource registry, execution lock, dedupe, HITL | Concurrent ranking script overwriting manual collection ordering |
| M-14 | Privacy-first tracking | Separate native event, network request, received report, consent state | Assuming custom Pixel fix eliminated standard Pixel token leakage |
| M-15 | SEO demand discovery | Search intent seed → query expansion → Chile Trends → GSC real query feedback | Publishing categories based only on invented keyword demand |
| M-16 | Experiment retrospective | Decision, implementation, observed result, disconfirmations, promotion/rollback | Repeating closed Logo or policy probes |

## Execution order for cold-start acquisition

1. Check commerce and ad eligibility, campaign review status and feed acceptance.
2. Confirm backend purchase truth and media attribution scope.
3. Confirm SKU inventory, price/promo, fulfillment and margin or approved market-probe subsidy.
4. Query account/search term data with a **completed local business day**; record partial-day separately.
5. Identify delivery vs relevance vs on-site abandonment, with denominators and sample sizes.
6. Select **one** action; constrain allowed fields and budget; secure approval.
7. Apply, read back, observe, record and avoid overinterpreting small samples.

Source: reusable best practices synthesized from Supermetrics analysis and campaign-management workflows plus MaxSensual incident reviews. This document is the adapted methodology, not a verbatim copy of plugin materials.
