# T16 生产推荐采集：可复用计量契约与非承诺范围

## 版本、作用域和时间

- Shopify MAIN 在 `2026-11-13T01:02:16.427Z` 切换为 `191909396758`；旧 MAIN `191900451094` 保留为未发布回滚主题。
- `collector_version=t16-v1.1`、`collector_revision=t16-consent-r1`、`deployment_environment=production`。
- **可信统计起点**：`2026-11-13T01:18:39Z` = `2026-11-12T22:18:39-03:00`。不得使用主题发布时间充当可信指标开始，历史/preview/旧采集器不合并。
- Shopify 官方后台 MAIN/readback + 技术仓库报告：`docs/T16-PRODUCTION-RESULT.zh-CN.md`；PostHog 只读对账 GitHub Action `43343742784`，生产 QA **11/11** UUID、43 字段一致。
- 推荐 `publishing_enabled=false`、`feedback.enabled=false`、`feedback.quality_approved=false`，只是观察采集上线；未启用新推荐排序或实时推荐服务。

## 指标定义

- `msx_rec_impression`：同 render 中卡片面积 ≥50%，连续 ≥1000ms，前台，分析 Consent 允许；同 render + product + position 唯一曝光键。100ms 几何复核只降低 IO 延迟的虚假曝光风险，非视线追踪、非全网络无损率。
- `msx_rec_click` 中 `product_open && qualified_view=true` 可与**服务端确实接收到的**同曝光键关联；快速点击、variant 选择、quick add intent、buy-now intent 都不是 Shopify 成交。
- 分子：有至少一次合格详情点击的 unique exposure keys；分母：合格且服务端收到的 exposure keys；分母 0 时 N/A；日汇总按分子分母重算，不直接平均商品 CTR。
- `is_internal=true`、已登记 `qa_run_id`、Preview、已确证测试 UUID、重复 UUID/曝光键冲突、不同来源或版本混用，排除整个曝光键；不把已知 QA 事件修改成消费者数据。生产 QA 接收 11/11、市场/反馈查询 0 行。
- 当前 `policy_id=unverified` 只能用于市场观察，不能冒充 `rules_v1`/`feedback_v1` 已经发布。没有推荐成交、收入或利润的可靠联接。

## 来源归因及隐私边界

- G2：只有已登记 UTM `utm_source=google&utm_medium=cpc&utm_campaign=g2-product-search` 识别为 PAID_SEARCH / G2。
- Google 合法格式 `gclid/gbraid/wbraid` 仅意味着 GOOGLE_PAID 证据，`campaign_group=UNKNOWN`；不通过点击标识推断 PMax。格式有效不等于向 Google 完成真实性认证。
- 无证据/冲突保留 UNKNOWN；已知搜索域可通过受控规则集推测 ORGANIC_SEARCH；未分类外部来源标 REFERRAL/unclassified，不能反推一定非广告。
- 不上传完整 URL/query/referrer、原始 click ID 或个人身份数据；QA 链接参数只是协作标签，不是安全认证。未标记 Agent 不能保证识别。
- 首次 Analytics Consent 拒绝不保存/发送推荐分析事件；撤回后清空旧来源并阻止在新 context 中使用旧曝光；重新允许新建 context。未审计所有第三方 Pixel/CMP/Safari 真机。
- **PostHog QA 隔离不覆盖 Shopify 标准电商事件、GA4 或 Ads。** T24-B 4 次 `add_to_cart` + 2 次 Checkout QA 需单独标注，不能用事件数直接减 Shopify session 统计。

## 商业数据下游约束

- 可信首要经营指标是独立验证、非测试客户付费订单；次要为扣除采购、实运、手续费、履约和广告成本的实际贡献利润。
- 仅凭 `human_or_bot_session=human`、加购、已进入结账、`PAID`、`test=false`、GA4 `purchase` 或 Google Ads Conversions，均不能证明真实外部消费者订单。
- 不做无共同稳定合法 ID 的 PostHog→GA4→Ads 事件级 JOIN；不得把 `syndicatedsearch.goog` 来源会话直接记为某个 PMax 点击。
- 保留 `America/Santiago` 和 UTC 时间、广告 CNY 与 Shopify CLP 货币、数据回填可能性；每次报表附查询窗口、是否完整业务日、数据缓存与观察层级。

## 实施责任

技术实现和原始受控 QA 证据归属 `hding12/maxsensual-recs`；本公开仓库只保存商家批准公开的业务脱敏约束、统计语义、时间/版本快照、链接及结论。不得复制带用户、支付、cookie、全链接的原始 PostHog payload。
