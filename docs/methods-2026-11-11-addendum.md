# 2026-11-11 实践后方法补充（M-17～M-25）

这是 `docs/method-catalog.md` 既有 M-01～M-16 的**增量**，而非新一套平行规则。每个条目区分观察、推断、允许执行的动作。来自 MaxSensual 的用户/执行 Agent/连接器案例；不是对插件原始文字的逐字复制。

| 编号 | 方法 | 输入和必要证据 | 严格禁止的推断 | 安全输出 |
|---|---|---|---|---|
| M-17 | **负证据复验** | 单次浏览器无事件→成功购物车请求/Shopify 事件/所有 Pixel 网络发送者/足够延迟/多次不同路径 | “没有抓到”=“全站未发送” | `INCONCLUSIVE`，补观察计划；真实缺口经重复证明后才提出代码修改 |
| M-18 | **电商事件唯一生产者契约** | Google & YouTube App、GTM、主题、Custom Pixel、Checkout Pixel 清单；同次 action 的 event ID、CID/SID、接收回执 | 用户身份一致=事件不会双计；单 Custom Pixel 去重 Set=全局去重 | 按业务动作和标准事件类型列生产者，禁止未验收的标准事件补发 |
| M-19 | **部署源码双表示校验** | 编辑区原始源码 hash，平台注入 wrapper 规则，保存后正文 hash，允许差异白名单，平台 readback | node syntax PASS 或保存成功=线上符合授权 | 明确比较对象；不符立刻回滚；不能事后放宽标准 |
| M-20 | **跨平台分母契约** | session/event/conversion/order，平台归因、业务日、货币、Bot/QA 分类 | Shopify cart sessions - GA4 ATC events=“漏数”；PAID=test=false=真实成交 | 单位可比时比较，不可比则并列报告与候选解释 |
| M-21 | **Search Partners 与 App placement 二层分母** | Search Partners 网络展示/点击/成本，placement 报表的 App/Website，时间窗口 | 昨年/上月 App 占比=当前广告占比；App 投放位置=Search Partners 点击来源 | 计算同窗口 353/2701 与 353/4835，分别命名分母；不批量历史排除 |
| M-22 | **同店多实验环境冻结/放行** | 活跃实验目标、变更时刻、影响页面、旧新商品快照、授权 | `apply=false` 试算=已发布；每个推荐更新都与购买实验因果独立 | 发布前 `APPROVAL_REQUIRED`；审核变更边界；记录发布版本与复核计划 |
| M-23 | **隐私与身份逐发送者审计** | CL consentPolicy、`init.customerPrivacy` 运行时状态、cookie 读取、发包、Consent 分支、个人信息字段 | CL 不要求先同意=所有会话无限制发送；代码没有 consent 字符串=必然违法 | 允许状态与实际代码/网络证据分开；fail-closed 但不等同“永不漏报” |
| M-24 | **单字段广告目标实验** | 精确 CampaignConversionGoal resource/updateMask、其他 goal readback、独立 campaign budget/status | 切 Purchase-only 后同日所有事件均归因于新设置；其他 Campaign 自动隔离 | 单变量起始点；第一整日 11/12；300 CNY/14天人工复核 |
| M-25 | **Agent 提议、用户授权、实际写入、平台读回四分法** | user scope approval、Agent report、platform raw API、GitHub Actions/result、回滚、时钟 | Agent 说“完成”=用户授权所有动作；GitHub job success=真实线上发布 | 分离 `PROPOSED/APPROVED/EXECUTED/READBACK_VERIFIED/ROLLED_BACK` 与 `VERIFIED/REJECTED/INCONCLUSIVE` |

## 真实实践与 Supermetrics 方法的关系

- 原 `marketing-data-queries` / `funnel-and-tracking-audit` 的**可迁移方法**是先定义报表单位、字段发现与时间范围，再把广告流量和 Shopify/GA4 购买证据对齐；T06 把跨平台不可比的口径明确写入约束。插件示例中的点击→会话差异 >25% 或平台/GA4 差异 >20% 只能触发诊断，不能直接判定漏报，更不能跳过实际购买核验自动重分配广告预算。`Supermetrics` 报表缓存和 normalized network flag 仍要与原生 API 并列记录；尤其核对 `requested_field_ids` 与 `canonical_field_ids`，因为别名映射可能悄悄返回不同指标，空值必须保留为 null 而非 0。
- `wasted-spend-audit` 的**适配原则**是搜索词→触发关键词→广告组→落地 SKU→实际形态，再决定限定范围的否词；此前 G2/G2X 精确排除已经在既有日志记录。T07 证明“placement 类别”和“network 类型”不能粗暴映射。
- `campaign-management` 的**实际约束**是 exact resource / update mask / user-approval / readback / campaign-level effect，T05 B-min 成功实现一变量实验，不能放大为全账户改动。
- `ecommerce-roas-analysis` 与 `budget-pacing-allocation` 的很多建议仍不能直接用于盈利排序：真实消费者成交基数为 0 时 ROAS/CAC 没有可解释的购买分母；300 CNY 是**人工复核触发**不是硬花费上限。
- `ad-creative-performance` 创意疲劳、创造性赢者判断等模板阈值并没有在 T05–T08 形成可信实验结论，不得因为插件有方法就标为已完成。
- T08 的**新增反例**：不先审计发送者，单纯提升埋点数量可能降低数据可信度。营销增长工作与技术实现的共同止损指标应该是**非测试消费者订单**，不是更多加购记录。

## 复杂问题的停止条件

- 已有更高质量的反证（如 App Pixel 已发一次），立即拒绝旧假设，不继续做 v6。
- 同类事故连续迭代时，从“技术实现可行”回溯“业务需求是否存在”；只修实现不验证前提会扩大风险。
- 所有生产变更遇到不符合预先定义的 SHA、状态、预算、授权范围，应当停止并回滚。即使最终业务事件正常，也不能绕过安全合约。
- 分歧必须记入 `records/insights` 的 `REJECTED` / `INCONCLUSIVE`，不能删除或悄悄覆盖旧报告。

关联：`docs/supermetrics-methods.md`、`records/methods-in-practice.md`、`docs/incident-lessons.md`、`records/daily/2026-11-11-full-review.md`。
