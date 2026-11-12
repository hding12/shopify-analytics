# MaxSensual | REC-CAPTURE-PROD 生产采集上线记录

- 记录日期：2026-11-12；业务时区：America/Santiago
- 证据等级：Shopify Admin 独立核验 + 推荐 Agent 上线报告（标注区分）
- 目标：曝光/商品点击采集基线，不发布新推荐、不启用反馈学习

## 上线状态

| 项目 | 事实 | 证据 |
| --- | --- | --- |
| 生产主题 | `191900451094` `MaxSensual Capture Only 2026-11-12`，`MAIN`，`processing=false` | Shopify Admin GraphQL 已独立读回 |
| 回滚主题 | `191496257814`，`UNPUBLISHED` | Shopify Admin GraphQL 已独立读回 |
| 发布时刻 | `2026-11-12T03:46:47Z` / `2026-11-12T00:46:47-03:00` | Agent 报告 |
| 前台生效确认 | 约 `2026-11-12T01:02:00-03:00` | Agent 报告 |
| 推荐商品自动发布 | `publishing_enabled=false` | 推荐仓库 `config/store.json` 已独立读回 |
| 反馈学习 | `feedback.enabled=false`, `feedback.quality_approved=false` | 推荐仓库 `config/store.json` 已独立读回 |
| GA4 事件镜像 | `false` | Agent 报告、采集模板源码 |
| PostHog 项目 | `727654` | Agent 报告 |

## 发布验收及限制

- Agent 报告：T12 两份正式主题文件 MD5 同步成功；全部 438 个已有文件中 431 个一致，3 个预期修改，4 个采集资源新增；广告、商品成员/排序、价格和支付配置未改。
- Agent 报告：PostHog 通过内部 QA 对账，集合页 16 次曝光、首页 15 次曝光及 1 次商品详情点击；QA 事件带 `is_internal=true` / `qa_run_id`，UUID 无重复。
- 上述记录是内部 QA，不是自然顾客流量的采集成功率；正常浏览器、长期弱网/物理断网、Safari、Consent UI 仍有未完全覆盖场景。
- 本次采集到的是**当前商品列表的曝光/点击基线**。未发布规则版推荐，不能将 `unverified` / `rules_v0` 的数据直接作为 `rules_v1` 推荐收益证据。

## PMax 实验干预边界

- PMax Purchase-only 原始开始：`2026-11-11T08:12:28Z`。
- 此次生产采集切换：`2026-11-12T03:46:47Z`，前台确认约 `2026-11-12T04:02:00Z`。
- 此次系观察性测量变更，不直接更改排序、支付规则或广告；但新增前端脚本，故应记入实验时间线。T12 展示文案改动此前已另行记录。
- 不重置 PMax 起点、不暂停观察；优先检验真实非测试订单、有效访客与贡献利润。

## 首页 Hero：经营者确认的业务承诺（保留，不要求修改）

- Shopify Admin 独立读回当前 MAIN `191900451094` 的 `templates/index.json`，MD5 `4a81222cadd46352a6154ff0c1b1ae02`：`msx_hero.settings.subheading = "30% off + envío gratis a todo Chile."`。
- **经营者于 2026-11-12 明确确认该 Hero 表述是业务口径、应保留。** 先前市场侧建议删除/改写 Hero 是不恰当的：错误地把现有技术实现当成了营销策略的最终来源。该建议已撤回。
- **需区分已确认的商业承诺与现有执行能力：** Shopify Admin 独立读回 30% 订单折扣为 `ACTIVE`，无门槛自动免运折扣也为 `ACTIVE`，但后者的 `combinesWith.orderDiscounts=false`。T10 内部测试单 `#maxsensual1004` 的商品折后 1,393 CLP，实际仍收 3,300 CLP 运费；当前结账对低额订单尚未验证能够兑现 Hero 的无门槛免运预期。
- T12 此前按“折后满 10,000 CLP 免运”修订的公告条、PDP 与 `/pages/despachos`，是目前结账能力的描述，而**不是已确认的最终营销政策**。如 Hero 保持无门槛免运承诺，需另行在商家承担的配送成本可接受前提下，对其他文案、折扣组合及真实 Checkout 进行一致性修复和验收；**不可仅靠改其他文案宣称已兑现免运。**
- 当前用户只要求更新市场记录，**未授权新增 Shopify 促销配置修改、免运叠加、重算价格、发布主题或广告更新**。推荐采集上线状态不受此事项影响。该业务一致性问题应并入下一次增长决策，避免继续反复开展技术排查。

## 记录状态

此文件由市场侧根据 Shopify Admin 读回与 Agent 报告形成。可复制到 `hding12/shopify-analytics/records/daily/2026-11-12-recs-capture-production.md`；GitHub 连接器写入尝试返回 403，因此当前**未推送**。
