# Applied methods vs plugin-provided methods vs insights

## Market insight categories

- **Audience and intent**: first active G2 Search clicked specific small/discreet/lipstick-shaped product terms; only three clicks at the time, not evidence of conversion or a winning market. Egg query in the A group demonstrated genuine intent query but target SKU form mismatch.
- **Availability constraint**: non-family-safe `APPROVED_LIMITED` restricted delivery, but 26 impressions and 3 clicks proved some live eligibility. Cannot infer all inventory is low quality or link high CTR to the restriction as a proved causal chain.
- **Search opportunity sizing**: Chile Keyword Planner reported approximate monthly averages for selected low-volume terms; market demand cannot be inferred by summing close variants, and third-party catalogue source availability needs live confirmation.
- **Offer and discount**: 30% automatic order discount overrode non-stackable BXGY code. Valid code remained ACTIVE yet did not yield promised buyer benefit during promo. Cart QA is operational truth.
- **Unit economics**: use CLP paid promotion price and actual landed COGS/fulfillment; source merchant retail COGS for market probes may be intentional subsidy. Corrected egg procurement breakeven under reported model: 11,691 CLP before freight or 15,191 CLP including 3,500 CLP source freight; revisit fees before negotiating actual bulk purchase.
- **Experiment design**: campaign-total 175 CNY is different from 25 CNY daily; test 7 days by actually eligible serving, stop at first independently verified paid customer order and use a delay buffer. One order proves one buyer, not repeatable demand.
- **Data quality and attribution**: `purchase=1` in GA4 was payment test; Merchant order was `PAID` with `test=false` but not a real external sale. ItemName split is fixed by item ID. Shopify funnel numbers must not be treated as event counts or sequential user journey.
- **Technical reliability**: micros scaling errors, normalized vs raw network flags, PDP range-delete regression, and concurrent ranking script risks all need first-class incidents and prevention rules.

## Supermetrics plugin workstreams — what was actually used?

| Workflow | Status in project | Basis |
|---|---|---|
| Query discovery / Google Ads campaign and search terms | APPLIED | Supermetrics actual campaign and term reads |
| Campaign management and safe readback | APPLIED | G2 and G2X checks, budget + status + policy review |
| Keyword Planner / demand discovery | APPLIED | Indicative CL monthly volume of egg and vibrador terms |
| Funnel & tracking reconciliation | PARTIAL | Shopify, Ads and GA4 reports; identity and buyer-order reconciliation incomplete |
| Wasted-spend search term relevancy | APPLIED | Egg term on non-egg A landing page → scoped negatives |
| Ecommerce unit economics | ADAPTED | Separate profit stock from information-buying sourced products |
| Blended ROAS / SKU profit ranking | NOT VALIDATED | G2 real paid orders 0, no trustworthy paid SKU revenue |
| Creative fatigue / creative winner testing | NOT APPLICABLE | Too few impressions and conversions |
| Budget optimization/diminishing returns | NOT VALIDATED | Below-budget spend and no reliable ROAS curve |
| Promo anomaly detection | NOT VALIDATED | No stable past profitable campaign baseline |

Do not call a workflow's default diagnostic thresholds a MaxSensual-specific discovered fact.
