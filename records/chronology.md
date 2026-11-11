# MaxSensual: G1→G2→G2X operational chronology (public historical reconstruction)

## Prior analytics and tracking work, Oct–Nov 2026

- ShopifyQL reports F01–F09, D01–D05, V01–V02 investigated session-to-checkout, UTM, channel×browser, payment attempts, product behavior and native report limits. In a documented Oct31–Nov09 window, Shopify reported 1,492 human sessions, 531 sessions with additions to cart, 523 sessions reached checkout and 0 completed checkout sessions. This is NOT a sequential user event funnel or a bot verdict.
- GA4 event/identity analysis separated native Shopify and GTM `cid+sid`, custom browser scripts, and Checkout custom `msx_vid` without canonical GA4 `sid`. Custom V2 removed raw checkout token output, but a separate standard pixel path remained a privacy concern requiring independent verification.
- Shopify collection quick-add and cart permalinks can bypass PDP view. Shopify `payment_attempts=0` may not capture outside provider attempts. Reports have different units and clocks.

## G1 and G2 startup, approximately Nov 10–11 2026

- G1 evaluated third-party sourced Kegel product ideas, but G2 prioritized three own-stock SKUs for first orders: A product `10655061278998`, B `10655062556950`, C `10655058690326`.
- A/B/C product copy improved with variants, factual specifications, FAQ; collections `recomendados`, `para-ella`, `vibradores-estimuladores`, `novedades` reordered. A local `rules_v0` ranking script could overwrite manual sort and was not to be run without coordination.
- Campaign `24447529143` `G2 · Product · Search`: Search only, budget 120 CNY/day, max clicks and 4.11 CNY CPC ceiling; AG-A `197334270890` + AG-C `199011811341`, ads `831240217886`, `831240217889`. Original CPC error (600 CNY instead of 600 CLP equivalent) corrected; platform ad review `APPROVED_LIMITED`, policy `NON_FAMILY_SAFE`.
- PMax Campaign #1 `24244298528`: preserved ENABLED, 42 CNY/day, adult-policy-limited; one prior 7-day snapshot recorded 3,059 impressions, 1,223 clicks, ~40% CTR, 257.83 CNY cost, without real customer orders. High CTR/cheap CPC alone did NOT establish bots or bad inventory.
- G2 Search first completed Chile business day Nov10: 26 impressions, 3 clicks, 11.93 CNY. Nov11 in-progress increased to 11 impressions, 1 click, 4.02 CNY in a later read. These figures are historical windows, not current totals.
- AG-B `202747853195`, ad `831286604810`, created PAUSED with conservative copy and 5 keywords; last reported policy review `UNKNOWN/REVIEW_IN_PROGRESS`.

## Promotion and checkout correction

- Shopify order-wide 30% automatic discount `1763977167126` and free-shipping automatic `1763977265430` extended through Nov30 23:59:59 Chile (`2026-12-01T02:59:59Z`). Original rules remained unchanged.
- BXGY code `G2PAR2` active but not combinable with 30% automatic discount, so A/B PDP advertising it was removed; code retained ACTIVE but not promoted during Nov promotion. Verify actual cart/checkouts; free shipping stacking remained `INCONCLUSIVE` without address input.
- A/B PDP HTML promo block deletion mistakenly swallowed specs and buying instructions. Restored from `PDP-ORIGINALS-before-promo-fix.json` snapshots. Verified post-repair A=1,517 and B=1,994 HTML chars, 5 and 7 list items, no residual bundle code, mobile smoke tests passed.
- A/B/C 30% promo paid prices observed: A 21,657 CLP, B 24,255 CLP, C 31,619 CLP. Promotion-period estimated pre-ad contributions A~10,641, B~12,217, C~16,685 CLP, contingent on the recorded fee/tax/cost model.
- Shopify order `#maxsensual1004` has `test=false,fullyPaid=true` but was independently identified as a merchant payment test. One GA4 Purchase later appeared for it (~14h processing lag). No validated G2 real customer orders at last observed window.

## Search term and policy diagnosis

- PMax limited status not caused by a previously disapproved business logo asset attached only to old paused Search Campaign `24246641229`; historic logo issue CLOSED NON-BLOCKING; do not delete old campaign.
- Actual G2 search terms included `vibrador disimulado`, `vibradores pequeños para mujer`, `vibrador con forma de labial`. Near-variant matching of `"vibrador discreto"` triggered `huevo vibrador` to non-egg A landing page and one ~4.02 CNY click.
- AG-A negative EXACT `[huevo vibrador]` and `[huevito vibrador]` were created and read back. Two new positive terms `"vibrador disimulado"` (AG-A) and `"vibrador labial"` (AG-C) created, while `[vibrador pequeño]` and `"vibrador con forma de labial"` hit `NON_FAMILY_SAFE` policy errors. A later pair of eligible terms remained no-impression at observation.

## Sourced-product model revision and G2X

- Three egg-shaped sourced products had placeholder Shopify inventory 100, but real availability depended on external merchants. Example primary SKU `15458888089878`, title `Huevo vibrador punto G con control remoto`, origin `erotik.cl`, list 27,990 CLP, promo 19,593 CLP, merchant source quote 18,990 CLP and estimated fulfillment freight 3,500 CLP. Simplified model estimated -7,299 CLP per promo order. This is a **test subsidy**, not a proof of poor category opportunity.
- Original margin-based AG-E NO-GO decision was expressly SUPERSEDED by user clarification: sourced catalog products are market probes, and low-cost real order signal can justify later manufacturer bulk buying. 2%/3% hypothetical CVR produced ~183–249 CNY per validated order; that is a forecast, not observed CPA.
- G2X `24459774700`, product experiment for egg shape, seven-day initial Nov12–Nov18 window, separate campaign-total budget 175 CNY `CUSTOM_PERIOD/LIFETIME`, CPC ceiling intended 4.11 CNY; starts PAUSED, never spend without ad approval.
- G2X was accidentally created with 411,000,000 CPC micros (411 CNY), corrected to 4,110,000 micros (4.11 CNY). Connector normalized partner network flag contradicted direct GAQL `target_partner_search_network=false`; preserve both and favor exact-field diagnosis rather than hiding conflict.
- Two `NON_FAMILY_SAFE` niche keywords initially failed normal creation; validateOnly showed `isExemptible=true`; a one-time official exemption request created `[huevo vibrador]` and `"huevo vibrador control remoto"` successfully. Keyword creation != ad review; RSA `831212776246` remained `UNKNOWN/REVIEW_IN_PROGRESS`, Campaign stayed PAUSED, 0 spend.
- G2X geographic option changed to `PRESENCE` through Supermetrics campaign update, `write_status=applied`, read back via connector. Ad approval still the launch gate.

## Explicit exclusions and authority boundaries

- Do not change PMax without explicit consent. Do not run ranking automation that overrides current Shopify merchandising. Do not promote `G2PAR2` during global 30%. No ExoClick recharge; no Mercado Libre adult listing or wholesaler outreach in this experiment.
- G2X campaign creation and eventual enable had conditional authorization: ad APPROVED/APPROVED_LIMITED, legitimate supplier and Shopify checkout, exact total budget, controlled CPC, Chile targeting and shipping.
- Each write should have before snapshot, scoped authorization, API status, independent readback and rollback. The G2X ads/AG-B remained in review in the latest user report; never treat that history as current live eligibility.
