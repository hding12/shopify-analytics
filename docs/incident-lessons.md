# Lessons worth preserving, not repeating

| Incident type | Verified mechanism | Durable safeguard | Avoid this inference |
|---|---|---|---|
| Discount conflict | Global automatic promotion takes precedence over a non-stackable bundle code | Cart/checkout test every combination, update customer-facing copy | Active discount code = usable discount code |
| PDP content deletion | Deleting from a promo heading to the next heading swallowed nested specifications | Snapshot + DOM target + required-section asserts + HTML diff/readback | “Removed coupon block” = only removed coupon block |
| CPC micros | Numeric scaling error made an intended CPC ceiling 100× greater | Unit tests, account currency, raw micros readback before enable | Connector number already correct |
| Network settings disagreement | Normalized plugin report disagreed with raw Google network fields | Record raw API & normalized fields, reconcile semantics | `search_partners:true` in one adapter proves actual partner traffic |
| Adult policy review | Some restricted keywords are accepted only via formal exemptible policy key | `validateOnly` → verify `isExemptible` → single authorized formal appeal → review state | Keyword created = RSA eligible or exemption guaranteed |
| Near-variant traffic | Broadening effect of close variants can send different product forms to same landing SKU | Query-level report + SKU relevance + scoped exact negatives | 1 click proves a category winner |
| Rare / incomplete data | First 3 clicks and a partial business day gave misleading early conclusions | Wait for comparable time windows and adequate samples | Near-limit CPC proves bid shortage; high CTR proves traffic quality |
| Analytics source fragmentation | GA4 item title changes split same product across rows | Aggregate by immutable item/product ID | New title = different product |
| Order identity | A merchant manual paid test can have `test=false`, `fullyPaid=true` | Maintain separate proof of external buyer intent | PAID = real customer order |
| Market probe economics | Dropship negative margin initially rejected an information-seeking SKU | Separate commercial profitability from R&D cost-of-learning | Negative first sale = invalid market test |
| Checkout/privacy | Fixing a custom pixel doesn't guarantee standard pixel no longer exports sensitive URL values | Independently inspect every sender and URL field | One fixed path means all paths are fixed |
| Hidden automation interference | Sorting automation could overwrite manual collection order | Resource lock / disable-while-editing / before-after snapshot | User-visible ordering stays unchanged |

This is a generalized lesson index. Selected account IDs, amounts and historical actions are publicly documented in `records/` with operator approval. Missing exact timestamps or raw provider evidence are not fabricated; credentials and customer PII must remain outside the public repository.
