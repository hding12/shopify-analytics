# 2026-11-13 方法论增量：M-26～M-34

> 继承 `docs/method-catalog.md` 的 M-01～M-16 和 `docs/methods-2026-11-11-addendum.md` 的 M-17～M-25。此处记录可移植的方法，不把 MaxSensual 的临时账户状态当成普遍规律。原始业务日：America/Santiago。

| ID | 方法 | 必要输入与执行流程 | 不允许的推断 | 产物与审批 |
|---|---|---|---|---|
| M-26 | **受时限保护的促销广告启用** | 广告 ID、广告组 ID、广告审核、账号与预算、保护脚本源码与 Enabled、`DRY_RUN`、调度时间和时区、UTC 截止、精确目标白名单；启用前重新读回，写入时仅变更广告状态，写后独立回读 | “脚本存在”=“已启用”；“调度 20–21 点”=“20:00:00 精准停止”；批准 2 条=批准其他广告 | 分离防护验证、广告状态写入和到期后真实暂停验收；启用和修改必须有单项授权 |
| M-27 | **来源证据阶梯与保守未知值** | 登记 UTM 组合→G2；有效格式 `gclid/gbraid/wbraid`→仅 Google paid evidence，campaign UNKNOWN；外部搜索引荐由固定规则集识别；不充分来源→UNKNOWN；来源身份与测试身份两轴记录 | 依据 GCLID 直接推断 PMax；把 referral=organic；把来源快照与真实广告点击/订单事件级关联 | PostHog 真实接收、各字段版本与规则集、Consent 状态、QA 排除；T16 仅推荐卡片曝光/点击，不是完整成交归因 |
| M-28 | **逐分析系统验证 QA 隔离** | 列出 Shopify、GA4、Ads、PostHog 各自产生者；检查每条系统的 QA ID/事件字段/接收端剔除；对事件数、会话数、订单数分别建账 | PostHog `is_internal=true`=Shopify/GA4 自动排除；4 个 add_to_cart event=4 个加购 session | 标出受污染时间窗口、事件级排除能力及无法精确回填的限制；不要从 session 指标减事件数 |
| M-29 | **联合可售性与变体级发布** | 父 Product ACTIVE、父渠道发布、变体库存和 `availableForSale`、**变体 `publishedOnPublication`**、选项/variant ID、Storefront JSON、真实购物车 | 父商品已发布+库存>0=每个子变体在该渠道可售；前台只出现一个颜色=主题 CSS 错 | 修复仅限目标变体和目标 Publication，保持其它渠道、价格和 SKU 不变；先只读，独立授权后写入与回读 |
| M-30 | **价格单位与结账权威口径** | Shopify 货币、Liquid 最小货币单位、自动折扣及数量/分摊规则；读取真实单件 Cart/Checkout→在同条件下推导整数舍入；测试卡片、PDP、JSON-LD、RSA 与到期回退 | 数学等价改写一定修复 1 CLP；单件模型完全代表多件订单；PDP 折后价可代替结账金额 | 用真实结算建立 price parity 矩阵和测试 fixture；改主题/广告需独立范围授权，RSA 改文案可能触发重新审核 |
| M-31 | **技术购买路径 vs 商业转化意图** | 手机 PDP→变体→Cart→优惠→配送地址→支付入口，用 QA 隔离；随后再分析非 QA 来源、商品竞争力和订单真实性 | 两款产品 Checkout PASS=没有购买阻力或已存在有效需求 | 拆成“机制可达 PASS”和“真实消费者订单未验证”；样本不足时不宣布胜出创意或加预算 |
| M-32 | **异常媒体指标多证据诊断** | 同业务日按网络类型展示/点击/成本、Google Invalidclicks、Shopify 来源与 bot 分类、GA4、后台订单；明示数据口径/无法 JOIN | 78% Search Partners CTR=欺诈；被标 human=已认证买家；syndicatedsearch.goog=某个 PMax 点击的确定映射 | 分层观察和人工复核门槛；异常仅触发诊断，不自动暂停/扩大预算 |
| M-33 | **多干预时间线与可信起点** | 用 UTC 与 Santiago 双时钟记录竞价、折扣、主题采集发布、促销 RSA、QA、变体渠道发布；记录可用数据起点和窗口完整性 | 有新干预的业务日仍是“单变量控制日”；发布即代表可信数据起点；前后比值证明某项改动因果有效 | 实验 `observed_interventions` append-only；保留 `first_clean_business_day=null` 直至验证无干预的完整业务日 |
| M-34 | **可证伪根因与证据升级** | 将缺色、价格错位、支付阻断写成假说；优先逐层对照原始 Admin 字段、发布关系、Storefront JSON、实际按钮行为；推翻时保留原结论历史 | 一项症状直接归因 CDN/索引/代理/主题；解决旧假说后删除失误记录 | `HYPOTHESIS → REJECTED/SUPERSEDED → VERIFIED`，写明反证和最小修复范围 |

## MaxSensual 样例（不作为通用真理）

- T22：两条 RSA `831439588688` / `831439627169` 在 Script `12708189` 到期防护下有限启用。G2 每日预算 120 CNY 未修改；截止 UTC 是 `2026-11-30T23:00:00Z`，脚本每日 20–21 CL 检查。**到期后的真实暂停尚未验证**。
- T16：新采集器 `t16-v1.1` 的生产可信起点是 `2026-11-13T01:18:39Z`；只采集推荐卡片曝光和产品点击，自动推荐排序/学习均关闭。PostHog 生产 QA 11/11 入库与排除通过，但不能推断未标记自动化全被识别。
- T24-B：两款已测 PDP/Cart/Checkout 支付前均可达，测试产生 4 次 Shopify/GA4 add_to_cart 事件及 2 次 checkout 访问，不能计真实流量；无订单。
- T24-C/D：`MS-MB-BLK-01` 有 15 件且 availableForSale=true，但 Online Store 变体发布 false，精确发布后恢复。全店当时审计 2,488 变体，仅该项符合“ACTIVE、有库存、但渠道未发布”的条件。
- T24-E：45,169 CLP 原价在 30% 活动下，真实单件结账为 31,619 CLP，而广告/页面曾为 31,618。修复仍处于草案阶段，不宣称已上线。

## Supermetrics / Shopify / GA4 的可迁移实践

1. Supermetrics 先发现 source/account/field/report type，检查 `requested_field_ids` 与 alias，记录 `cache_used/cache_time`；写后尽量用 fresh 查询并独立读回。只改变白名单字段，保留其他配置快照。
2. 按 `Networkwithsearchpartners` 分流，结合 `Invalidclicks` 与可靠消费者订单检查流量；Google 报告无效点击也不能证明其余点击真实。报告网络表、来源域名和订单分别注明分母，不做无共同键的事件级 JOIN。
3. ShopifyQL `sessions_with_cart_additions` 是会话数；GA4 `add_to_cart` 是事件数；Admin Abandoned Checkout 是独立记录；Google Ads Conversion 可以不是 Purchase，需读转化动作定义。
4. 用户授权绑定精确资源、字段和时间。原 T16 仅采集发布许可不能扩张为 `rules_v1` 推荐；T24-D 变体 Online Store 发布不能扩展为 Google & YouTube 渠道。
5. 止损原则：确认原始商业需求存在后再写代码。对同一问题持续发起“技术修复”前，先寻找对原假设的反证。

## 相关资料

- `docs/supermetrics-methods.md`（已应用工作流 vs 插件可用模板）
- `docs/measurement-t16-production-contract.md`（T16 数据契约与边界）
- `records/daily/2026-11-12-t20-t22-promo-rsa.md`
- `records/daily/2026-11-13-t16-t25-growth-review.md`
- `state/guards-2026-11-13-addendum.json`
- 私有技术仓库 `https://github.com/hding12/maxsensual-recs` 的 T16 生产报告（公开控制仓库仅保存脱敏摘要和链接，不复制原始数据）
