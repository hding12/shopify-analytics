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

<!-- T26 2026-11-13 -->
## 2026-11-13 新增失误与长期保护

| 事件 | 已证实机制 | 防重犯规则 |
|---|---|---|
| 有货黑色变体不显示 | 子变体未发布 Online Store，虽然 ACTIVE 产品、库存>0、`availableForSale=true` | 检查**子变体发布表**、父商品渠道发布和前台变体 JSON；不要直接归因 CSS/缓存或重建 SKU |
| PostHog QA 隔离成功但 Shopify/GA4 污染 | `is_internal` 仅推荐 collector 有效，电商标准事件另外收集 | 各平台逐接收端验证 QA 标志；无法从 session 汇总直接减去 event 次数 |
| 促销价差 1 CLP | 主题卡片/PDP/JSON-LD 的独立 CLP rounding 与 Shopify 单件折扣取整不同 | 使用官方子单位与实际结账对照；覆盖所有价格触点；补丁未验收不可记已部署 |
| Search Partners 超高 CTR / Checkout 到达 | 网络点击、来源会话、GA4 事件、真实客户订单分母不同，Google 另记录 invalid clicks | 多层验证，避免以高 CTR/“human”标签推断诈欺或购买意图 |
| T16 主题上线时间混同可信数据起点 | 主题成为 MAIN 在真实接收端对账前 | 单独记录发布 UTC 与质量门槛 PASS 后的 `trusted_since`，生产 QA 不能计消费者 CTR |
| 防护脚本到期与促销结束不同时 | RSA 保护计划 11/30 20:00 CL，Shopify 折扣到 23:59:59 CL | 两条独立未来依赖分别读回；不能假定精确 20:00 暂停或促销自动文案同步 |

黑色变体和 T16 的正向结果只说明此次范围内验证通过，不能外推为 Shopify 全部渠道永久正常。
<!-- /T26 2026-11-13 -->
