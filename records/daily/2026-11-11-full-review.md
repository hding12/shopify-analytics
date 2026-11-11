# MaxSensual — 2026-11-11 增量全量审计索引

> **资料类型：事件重建与知识增量，不是原始平台审计日志。** 统一以 `America/Santiago` 为业务日期；准确时间仅在有可靠证据时记录。公开仓库不得包含凭证、客户身份、订单地址或完整 Checkout URL。已有历史记录不重写；本补丁保存今天新增、纠错与归档的内容。
>
> **本次范围：** G1/G2/G2X 旧记录的覆盖核查 + T05/T06/T07/T08 + PMax Purchase-only + 推荐系统试算与 PostHog QA + 市场总控首次 GitHub 发布。**不执行** Google Ads、Shopify 或推荐仓库写入。

## 1. 按证据强度划分的最终状态

| 事项 | 当前结论 | 证据类型 | 不得推断 |
|---|---|---|---|
| PMax `ADD_TO_CART~WEBSITE` 转化目标 | 执行 Agent 报告：单目标 true→false，原 Google API 读回通过；PMax Enabled、42 CNY/日另有连接器读回 | 原生 API Agent 报告 + 独立目标以外字段读回 | 不能把 11/11 全天算作新策略实验 |
| Shopify 4 笔历史订单 | 用户确认均为内部测试；消费订单 0，真实消费者收入 0 CLP（当次基线） | 经营者正面确认 | Shopify `test=false` 或 `PAID` 证明真实买家 |
| Shopify/GA4 加购落差 | 不同单位/归因口径；差额不能用于判定漏报或 Bot | ShopifyQL + GA4 诊断 | 用 473 个“加购会话”减 141 个 GA4 事件得漏报量 |
| PMax 移动应用位置 | 当前窗口 353/2701 可枚举投放位置 = 13.1%；占 4835 总展示 = 7.3% | T07-R 修正后 Agent 报告 | 全站 99% 当前曝光为手游；Search Partners=游戏 App |
| T08 Custom Pixel 补发 | 生产中 App Pixel + Custom Pixel 各发 1 次，导致重复。准确回滚由 Agent 报告验证。 | 执行 Agent 网络对照 + 回滚读回 | 原 App Pixel 缺失集合页加购；需要继续开发 v6 |
| 推荐 `rules_v1` | Github Actions 26 位试算、0 阻塞，`apply=false`，`msx-state.applications=[]`；未正式发布 | 已连接 GitHub run/分支直接读回 | GitHub run success=顾客端已换榜 |
| PostHog | 私有 QA 主题内部曝光点击可见，学习关闭且样本不足 | 推荐私有仓库已提交 QA 记录 | QA=真实消费者偏好 / 可用于利润优化 |
| Growth Control v1 | 市场仓库 commit `a851497...`；CI 校验通过，3 模块、2 实验、5 任务 | 连接器直接读取 GitHub commit/日志 | `check-change` 是 Shopify/GitHub 自动锁 |

## 2. 今天实际生效的 Google Ads 变更：T05 / B-min

- Campaign：`24244298528`；Ads account：`7828819394`；账户结算币种：**CNY**。
- 用户明确批准且执行 Agent 报告于 **2026-11-11 05:12:28 -03（08:12:28 UTC）** 修改精确对象：`customers/7828819394/campaignConversionGoals/24244298528~ADD_TO_CART~WEBSITE`。
- 变更：`biddable: true → false`，Update Mask 仅 `biddable`；系统将 campaign goal config level 从 `CUSTOMER` 切为 `CAMPAIGN`。`PURCHASE~WEBSITE` 保持 `biddable=true`；不得外推其他 campaign、account conversion action、预算、状态被修改。
- Supermetrics 单独读取该 PMax 为 `ENABLED`、`42 CNY/day`、`MAXIMIZE_CONVERSIONS`。两种证据不能互相替代。
- **首次完整新策略业务日：11 月 12 日（智利）**。11 月 11 日是前后混合数据；不得给 05:00–05:59 整小时贴“后变更”标签（写入在 05:12）。
- 人工复核：**新增花费 +300 CNY 或 14 天（约 11/25）先到**；这不是自动预算上限，也不是强制停投或关机时间。实际累计花费和当下广告状态需要新读回。
- G2 Search `24447529143` 及 G2X `24459774700` 不在这次变更范围。G2X 最后报告 `PAUSED`，广告审核和履约条件未通过前不启用；原先“关键词豁免创建成功”不等于广告审核通过。

### 内部订单污染隔离

| 内部订单引用（无顾客信息） | 实付 CLP | 分类 |
|---|---:|---|
| `maxsensual1001` | 3,301 | PAYMENT_TEST |
| `maxsensual1002` | 3,301 | PAYMENT_TEST |
| `maxsensual1003` | 4,000 | PAYMENT_TEST |
| `maxsensual1004` | 4,693 | PAYMENT_TEST |
| **合计** | **15,295** | **4 笔内部测试；真实消费者订单 0** |

这些订单保留在财务账里；不得作为外部购买、ROAS/CAC 的分子。任何新订单都要独立核验，不继承这四单的分类。

## 3. T06 转化漏斗与真实观察边界

**业务窗口 2026-10-29～2026-11-11，按各平台查询定义。**

| 数据平台与过滤器 | 会话数 | 含加购会话 | 到达结账会话 | 完成付款 |
|---|---:|---:|---:|---:|
| Shopify `referrer_domain=syndicatedsearch.goog` | 1,097 | 473 | 467 | 0 |
| Shopify `human_or_bot_session=human`（上述来源） | 1,049 | 453 | 447 | 0 |
| Shopify `human_or_bot_session=bot`（上述来源） | 48 | 20 | 20 | 0 |
| Shopify `referrer_domain=google.com` | 365 | 109 | 106 | 0 |

GA4 总源分组概览：**2,732 sessions、141 次 `add_to_cart` events、83 次 checkout 事件、1 次已确认内部测试 purchase**；`google/cpc` 1,515 sessions、35 次加购事件。GA4 的 `add_to_cart` 是事件，Shopify 的“有加购的 sessions”是会话分类；不同来源属性、归因、Bot 分类、用户授权也不完全一致。不得直接相减生成虚构的漏报率。

ShopifyQL `payment_attempts=0`（11/1–11/10）与已知实际付款测试不一致，外部支付方式的覆盖范围仍是 `INCONCLUSIVE`；不可据此宣称用户没有尝试支付。未完成的 Checkout 身份记录不是可独立认证的真实客户。

## 4. T07 / T07-R：流量质量不能靠错误分母判断

| 网络（10/29–11/10） | 展示 | 点击 | 花费 CNY | 单独报告的 filtered invalid clicks |
|---|---:|---:|---:|---:|
| Search Partners | 2,753 | 1,582 | 275.6155 | 193 |
| Google Search | 556 | 58 | 102.1490 | 3 |
| Display | 1,526 | 70 | 5.9252 | 71 |
| **合计** | **4,835** | **1,710** | **383.6897** | **267（不能再从已计费点击中减去）** |

历史 37 个广告归因转化均为加购，**非真实消费订单**。Search Partners 高 CTR 是调查信号，**不是** Bot、无效流量或真实购物意愿的定论。

最初 T07 误用全量历史 319,869 个 placement impressions，其中手游/移动 App 大多来自 9/13–10/17；误报“当期 99% 为手游”，随后 T07-R 修正：当期可枚举 placement 为 **353 mobile app + 2,348 website = 2,701**，占当前总 PMax impressions 的分母为 **4,835**。可枚举投放位置不覆盖整个网络报告。移动 App 属 CONTENT/Display，不应混同 Search Partners。**禁止仅因这些历史数据批量排除约 1,636 个 App**（可能具有账户级副作用）。

PMax 新 Channel Prioritization/Budget Allocation 控件在该账户是否可用仍不确定；API `UNRECOGNIZED_FIELD` 只说明所测字段不可用，不是 UI 不存在的证明。

## 5. T08：一次完整失败实验被生产证据否定

详见 [T08 生产事故专页](../../docs/incidents/T08-2026-11-11-production-rollback.md)。要点：

1. 初始假设：集合页 `/cart/add` 成功而单次抓包没有 GA4 `add_to_cart`，推断漏报。**该假设后被 REJECTED**。
2. T08-R1：发现原 Custom Pixels 使用 `msx_vid/msx_sid`，与页面 `_ga` 身份不同，初始直接补发会导致身份碎片化。B′ cookie 方案经过 fail-closed 设计，但必要性仍未证明。
3. R2/R2b/v5：修正 Consent、身份、完整集合路径、`epn.value` 编码、自动折扣金额冲突，所有静态测试通过，仍未检验事件生产者是否唯一。
4. 生产执行 Agent 报告：App Pixel 和自定义 Pixel 对同一次集合加购各发送一次，导致双计；与此同时 Shopify 保存后源码 SHA **不等于授权预期**（平台注入代码）。按协议恢复线上 Pixel 原始 SHA，并验证回复 1 次 App 事件。
5. **结案：部署失败、Agent 报告回滚成功；不再据此推行任何 Custom Pixel 补发。** 未独立验证 GA4 全部会话都完整采集，未解决所有跨平台差异。

关键原则：同一业务操作必须先识别全部生产者（Google & YouTube App、GTM、主题、Custom Pixel 等），再考虑新增发送者；网络请求、身份匹配、GA4 接收和业务归因分别验收。

## 6. 推荐技术仓库：已试算，未发布，之后改为只读参照

- 技术库 `hding12/maxsensual-recs` **Private**；市场库 `hding12/shopify-analytics` **Public**。当前用户要求：不修改或继续触发推荐仓库；市场侧只读参考，未来再研究协作。
- `rules_v1` 最新 Github Actions [run 43004092227](https://github.com/hding12/maxsensual-recs/actions/runs/43004092227) 第 2 次尝试 **2026-11-11 10:49:05 UTC** 成功；`APPLY=false`、`initialize_state=false`、26 placements、0 publish blockers、计划 `02a5e78282e8b0a27c1df9f3`。其 `msx-state/applications=[]`。
- 当前版本识别 38 件自有可售产品、333 件供应商现货；首页 10 位、严格 2 个自有位，全面按供货与可售库存筛选。5 件缺货排除。源文档关于早期 37/38 active 的矛盾以最近正式核验与实际 Shopify 现场读回为准。
- **如果**全量发布，首页 10 个原产品可能完全更替，主要 PMax 落地页 `para-ella` 等前排也会显著变动，影响独立的 Purchase-only 增长观测；发布前必须说明受影响 URL、商品排序、用户影响和新测量边界。
- PostHog 项目 `727654`（US Cloud）是可替换的行为信号；QA 主题 `191875711254` 为未发布主题，`internal=true`、GA4 镜像关闭。内部 QA 事件不是实际销售，也不应参与推荐学习。
- `publishing_enabled=false`、反馈学习关闭、正式自动调度未启用。不要因“0 publish blocks”自行改开关；现阶段禁止触发任何推荐写入。

## 7. 市场仓库作为唯一业务决策索引

- 市场库提交 [`a851497`](https://github.com/hding12/shopify-analytics/commit/a851497f03e8253493c43aa1c95b29bf187da9e9) 增加 `control/portfolio.json`、`experiments.json`、`tasks.json`、`integrations.md`、`control/README.md`、只读检查脚本、CI。
- [CI run 43012873391](https://github.com/hding12/shopify-analytics/actions/runs/43012873391) 实际校验通过：3 模块、2 实验、5 任务。
- `control/experiments.json` 的 `APPROVAL_REQUIRED` 是人工决策提示，不是对 Shopify/GitHub 的技术锁；任何市场仓库快照不构成生产写入授权。
- 当前两个仓库保持分离，无新数据库、消息总线或自动双向同步。**技术 Agent 并不因市场仓库中有决策文本就自动受到远程权限管控。**

## 8. 旧工作已经归档，无须本次重复

| 范围 | 现有仓库位置 | 本次处理 |
|---|---|---|
| G1/G2/G2X 搜索和广告操作 | `records/chronology.md`, `records/runs/2026-11-g2-g2x-reconstructed.jsonl` | 保留历史，不重复计入今天新增的真实写入 |
| 关键词豁免 `isExemptible`、正式申请 | `docs/method-catalog.md` M-08, `docs/supermetrics-methods.md`, `records/insights/insights.json` INS-MS-004 | 明确持续有效的原则：创建关键词 ≠ RSA 已审核，也不是策略豁免成功投放 |
| 负面关键词精确匹配、产品形态错配 | `records/runs/2026-11-g2-g2x-reconstructed.jsonl`, `docs/incident-lessons.md` | 保留细粒度 ad-group 对象与观察不足限制 |
| Google Ads CPC micros 100× 错误与纠正 | `records/chronology.md`, `docs/incident-lessons.md`, `records/insights/insights.json` INS-MS-005 | 不重复修改当前 CPC |
| 30% 自动折扣与 G2PAR2 冲突、PDP HTML 修复、Checkout 运费不确定 | `docs/incident-lessons.md`, `records/chronology.md`, `docs/analytics-application.md` | 方法保留；实际优惠/支付按新平台读回判断 |
| 双轨业务经营：自有库存盈利、供应商现货信息成本 | `docs/business-model.md`, `records/decisions/decisions.json` | 与 Purchase-only 实验区分业务目标 |
| Supermetrics 诊断与预算、创意、SEO 方法论 | `docs/supermetrics-methods.md`, `records/methods-in-practice.md` | 保留是否实际 APPLIED vs NOT VALIDATED 状态；不把插件模板阈值当成事实 |

## 9. 后续工作分工与限制

- **当前优先：** PMax 从 11/12 智利自然日起的真实消费者订单、花费和流量质量跟踪。
- **测量：** 不再开发 T08 v6；T09 若执行必须先获得实际任务授权且保持只读，不能将提议标记为已完成。
- **推荐：** 只读参考。任何真实发布需新的用户明确授权和营销实验冲突评估。
- **GitHub：** 本补丁只更新市场仓库的知识与验证脚本；不触发任何远程技术任务。

**关联结构化文件：** `records/runs/2026-11-11-operations-addendum.jsonl`、`records/decisions/2026-11-11-addendum.json`、`records/insights/2026-11-11-addendum.json`、`state/guards-2026-11-11-addendum.json`。每个来源仅按本轮证据可支持的强度归类，未提供原生 API 原始快照时，不编造请求哈希。
