# Applied analytics — measurement is not an attribution shortcut

The existing `AGENTS.md` is authoritative for field definitions and tracking/privacy safety. This document gives the workflow in practical order without duplicating those definitions.

1. ShopifyQL `sessions`: visit/cart/checkout-reaching sessions. A session with cart additions is not the `add_to_cart` event count.
2. ShopifyQL `sales` + Admin orders: backend revenue and paid-order evidence. Distinguish platform test orders and real merchant payment tests from external customers.
3. ShopifyQL `payment_attempts`: payment attempts recorded by that dataset; outside processors may not be completely represented.
4. GA4: reports received events; inspect source scope, original item ID, transaction ID, timestamp and processing lag; do not assume all ecommerce events mapped correctly.
5. Google Ads: paid impressions, clicks, campaign and network fields, creative review, policy, keyword/search terms and conversions; avoid interpreting `Conversions` as backend purchases without reviewing conversion actions.
6. Cross-source: align date range, timezone, account currency, joins and sample. Unmatched data is `UNKNOWN`, not automatically fraudulent or invalid.

**Buyer path warning:** Collection quick-add or cart permalink can reach checkout without a PDP view. Funnel ratios built from landing-page aggregates are not true SKU-based user journeys.

**Pixel warning:** Shopify standard pixel, GTM, custom body script and custom Checkout pixel may use different `cid`/`sid` identities. An event sent on the network is not automatically present in the expected GA4 session. Do not send checkout tokens, emails or identifiers in event parameters/URLs.

**Privacy and validation:** Check real deployed code and shop privacy settings, test legitimate consent flows, observe actual network requests, read back deployment, and avoid inferring global safety from one custom Pixel fix.
