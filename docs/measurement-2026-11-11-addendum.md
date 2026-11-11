# 2026-11-11 测量契约修订：先区分实体，再判断漏斗与归因

## 平台、单位与来源

| 数据 | 单位 | 可直接表示 | 不足以表示 |
|---|---|---|---|
| Shopify session with cart additions | 会话 | 此次会话至少一次加购 | GA4 `add_to_cart` 事件条数 |
| Shopify session reached checkout | 会话 | 会话触发过结账行为 | 付费尝试必然发生、真正购买意愿 |
| GA4 `add_to_cart` | 事件 | GA4 接收且计量到的加购行为 | Shopify 的唯一用户/会话、已付款客户 |
| Google Ads `Conversions` | 依广告动作与归因规则 | 归因到广告的指定转化 | 实际 Shopify paid 订单（需审视 action 名） |
| Google Ads Invalid Clicks | 过滤的点击 | 平台识别/过滤的无效交互 | 可再从计费 `Clicks` 中直接扣除的数量 |
| PMax placement impressions | 可枚举位置展示 | 部分网站或 App 投放位置 | 整个 PMax 网络级展示或 Search Partners 点击分布 |
| Shopify order fully paid | 订单财务状态 | 有支付或财务记录 | 外部消费者、真实需求、归因 ROAS |
| ShopifyQL `payment_attempts` | 指定报表可见尝试 | 在其覆盖范围内的尝试 | 外部支付提供商全部支付行为 |

跨平台比较必须有 `source`、`account`、`business_timezone`、`window`、`filters`、`attribution`、`unit`、`denominator`、`test_classification`、`captured_at_utc`。需要新鲜数据时禁止用缓存冒充当前。

## 当前有效的证据约束

- Shopify 10/29–11/11 `syndicatedsearch.goog`：1097 sessions / 473 cart sessions / 467 checkout sessions / 0 completed。`human` 1049/453/447，`bot` 48/20/20。这是 Shopify 的人/机器分类，不是诈骗或假流量的独立鉴别器。
- 同期 GA4 概览：2732 sessions、141 add_to_cart events、83 checkouts、1 QA purchase。`google/cpc` 1515 sessions / 35 ATC events。不能跨模型构造“473 vs 141 有 332 次加购漏发”。
- 历史 Shopify 四单全部内部测试：金额 CLP 3301/3301/4000/4693（总 15295）；真实消费订单 0、真实消费者 CLP 0（当时窗口）。
- Google Ads Oct29–Nov10：Search Partners 2753 impressions/1582 clicks/275.6155 CNY；Google Search 556/58/102.149 CNY；Display 1526/70/5.9252 CNY；37 conversions 全部 ATC。不能用其证明真实购买。
- 网络级展示 4835、可枚举位置级展示 2701、mobile-app 353；两个分母分别给 7.3% 和 13.1%，都需标注。
- 原始 PMax 配置 `PRESENCE_OR_INTEREST`；G2X 用户要求和 Agent 读回 `PRESENCE`。不要把不同活动的定位配置混用。

## 事件链实验：四道证据门

1. **业务行为**：是否有成功 `/cart/add`，是否收到 Shopify `product_added_to_cart` 标准事件？
2. **发送者归属**：观察 Google & YouTube App、主题/gtag、GTM、Custom Pixel 等所有 `/g/collect`，辨认独有标记与重试。
3. **用户与会话身份**：CID/SID 是否匹配预期？单次业务操作是否多生产者上报？
4. **接收与报表**：DebugView 或实时事件、商品 `item_id`、数量、币种、事件数是否一致？延迟是否影响可见性？

每一层失败时首先报告 `INCONCLUSIVE` 和可能的替代解释，而不是自动写补丁。只有证明原生或 App Pixel 没上报，且排除重复事件发送者，才有“新增补发器”的候选需求。

## 优惠价格与加购价值

PDP 实测商品 `pr=30938`，页面折后显示 CLP 21,657；30% 自动折扣涉及商品显示、购物车行成本和 GA4 电商价值之间的不同口径。即使网络中 `epn.value=30938` 被接收，也**不能**直接代表消费者真实付款金额，更不能计算贡献利润。金额口径修复应独立成单独实验，并与双计事故切开。

## 决策要求

- 订单真实与否：以经营者/后端独立证明为准，不用订单状态字段或 GA4 purchase 单独决定。
- 投放质量：相关性、投放位置、付费成本、客户真实购买分别观察；不把“异常 CTR”直接等同机器人。
- 新收集的推荐曝光：PostHog 内部 QA `is_internal=true` 不用于推荐学习；实际曝光率、点击和购买效果应与广告/营销变更分开归因。
- 推荐排序变更：作为 **第二个实验变量** 记录时间、集合、首屏 SKU、落地页和版本，以免将变化全归到 PMax 出价目标上。
