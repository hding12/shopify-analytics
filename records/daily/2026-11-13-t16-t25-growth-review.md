# 2026-11-13｜T16 生产采集、T23–T25 漏斗 QA 与商品变体修复

这是 2026-11-12～13 期间多个互相影响的变更与 QA 的**脱敏事实记录**。不能把两天当成单一变量实验；报告数字是给定查询时刻的历史快照，平台可回填。时区 America/Santiago，广告 CNY、Shopify CLP。

## T16：仅推荐曝光采集发布（不等于推荐策略上线）

- 新 MAIN：`191909396758`，发布 `2026-11-13T01:02:16.427Z` = CL 11-12 22:02:16；旧 MAIN `191900451094` 保留 UNPUBLISHED。
- 生产采集版本 `t16-v1.1`、修订 `t16-consent-r1`；QA 真实接收 11/11 UUID、43 字段一致；首次拒绝分析期间推荐零事件，市场与反馈查询对 QA 均 0 行。
- **可信生产观察起点不是发布时刻**：`2026-11-13T01:18:39Z` = CL 11-12 22:18:39；旧测试/preview/无来源历史不能回填。
- 推荐排序发布 `publishing_enabled=false`、反馈学习 `feedback.enabled=false`、质量批准 `feedback.quality_approved=false`，三个不同开关仍关闭。
- 私有技术仓库证据：`https://github.com/hding12/maxsensual-recs/blob/main/docs/T16-PRODUCTION-RESULT.zh-CN.md`、`https://github.com/hding12/maxsensual-recs/actions/runs/43343742784`。

## T23：对漏斗数字与真实消费者的区分

- Shopify Admin 目前仅有四笔已知商家 QA 支付订单 `#maxsensual1001`–`1004`；**没有独立核实的真实消费者订单**。
- 部分 G2 UTM 会话表现为商品页浏览但没有加购。某次日本首页自引荐触发加购/进入结账，不能算 Google 付费消费者转换。
- 查到三条当时的 Abandoned Checkout，均已有 Shopify 恢复邮件 SENT，后续完成订单 0；部分为 QA 或身份不确定。不能公开客户身份、Checkout ID 或明细，不应再次自动发送营销消息。
- Shopify Sessions、GA4 events、PostHog recommendation events 和真实订单不是同一口径；不跨系统强行 JOIN。

## T24-B：手机购买路径在已测条件下通过

- Agent 使用 390x844 移动视口实际验证 G2 两款商品，PDP→Cart→Checkout 支付前流程均 PASS；30% 折扣、标准运费 0、两个支付入口可见，没有提交支付、联系邮箱或真实订单。
- Mini Bullet 原价 30,938 CLP，显示/结账均为 21,657 CLP；口红款原价 45,169 CLP，PDP/广告 31,618 CLP，但 Cart/Checkout 31,619 CLP，差 1 CLP。
- 发现商品描述仍写 `Envío: gratis en compras desde $10.000`，与活动 `sin mínimo de compra` 冲突；PDP 上 `3–5 días hábiles` 与政策允许的更长履约周期口径不一。两项需内容修改授权。
- QA `qa-t24b-20261112-a` / `-b`，CL 11-12 08:35–09:05：PostHog 推荐事件带 QA 身份，但 **Shopify/GA4 标准 add_to_cart 4 次和 checkout 访问 2 次没有同等 QA 隔离**。记录为污染窗口；不能直接从 session 统计中减 4 或 2。
- Cloudflare 429 曾阻挡自动化环境 `/cart/add.js`/Checkout 约 8 分钟；是环境相关已观察异常，**不能据此排除真实 VPN/代理访客风险**。

## T24-C/D：黑色变体真正根因与受控修复

- 初步假说：Shopify Storefront 索引或 CDN 异常。通过 Shopify Admin GraphQL 发布关系查明实际根因：Mini Bullet Negro `gid://shopify/ProductVariant/51641609355542` 存货 15、`availableForSale=true`，但 `publishedOnPublication(Online Store)=false`，并非缺货。
- **T24-D 精确 mutation**：`2026-11-13T03:04:49Z` = CL 11-13 00:04:49，使用 `publishablePublish`，目标仅该变体与 Online Store Publication `313209422102`。写前 false、写后 true，Shopify Admin 独立回读 true；Rosa `51641609322774` 一直 true，库存均 15，售价均 30,938 CLP。
- 前台独立 QA：`.js` 返回 Rosa + Negro，两个 radio，切 Negro 后 ID 不回落，价格/加购入口可用。
- Google & YouTube / Shop / POS 仍未为 Negro 发布。这次授权仅 Online Store，不得追认或外推其他渠道发布。
- 全店只读逐变体审计 **2,488 个变体**，该时点只有上述 1 个符合“ACTIVE 商品、有库存、Online Store 未发布”的同类异常。其他 2,092 个 ACTIVE 变体库存 0 是另一类库存问题，**不是同一种渠道发布故障**。

## T24-E 尚未实施的价格一致性修复

- 口红款 Checkout 实收 31,619 CLP，当前 G2 促销 RSA `831439627169` 标题 `Precio final $31.618`，PDP / 商品卡 / JSON-LD 亦为 31,618 CLP。
- **重要技术反证**：在 Liquid 的原始子单位上仅做 `base × 70%` 与 `base − floor(base × 30%)` 的数学改写，并不足以保证最终整数 CLP 与 Checkout 一致。方案必须先按 CLP 整数规则验证、再转换回钱币子单位，并覆盖 card / PDP / JSON-LD；多件订单需独立校验。
- 本项为 `PROPOSED`，没有主题改动；RSA 改文案可能重新审核，必须单独授权。**禁止把 T24-E 写成已修复。**

## T25 增长观察与未获支持的因果结论

- 11-12 G2 Search 18 clicks、164 impressions、70.32 CNY；促销 RSA 合计 7 clicks、27.85 CNY，Google Ads conversions=0。
- 11-12 PMax 后续回填 162 clicks、276 impressions、34.0017 CNY；Search Partners 157 clicks、199 impressions，Google Invalidclicks=19。
- Shopify 来源 `syndicatedsearch.goog` 11-12 有 111 sessions、47 add-to-cart sessions、46 reached checkout、0 completed checkout；此来源域名**不能**与 PMax 点击作事件级绑定，human 标签也不是已验证身份。
- 继续以第一笔非测试消费者付款订单和可验证贡献利润为第一目标，切勿据 QA 加购、高 CTR 或小样本 RSA 直接扩大广告预算。

## 需继续检查的两个真实未来依赖

1. Google Ads Script `12708189` 对两条促销 RSA 的实际到期暂停：`2026-11-30 20:00 CL` 开始符合截止，20–21 CL 调度；截止后独立回读实际状态。
2. Shopify 促销折扣与无门槛免运费在 `2026-11-30 23:59:59 CL` 到期后，检查 Hero/PDP/商品描述/广告承诺是否已经同步；广告时限与 Shopify 活动结束时间不同。
