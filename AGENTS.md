# AGENTS.md — MaxSensual Analytics

<!-- T26 2026-11-13 -->
## 最新入口：T26 2026-11-13（覆盖下面旧时点的执行状态）

**开始新增长任务前**：先读 `control/README.md` 与 `state/guards-2026-11-13-addendum.json`，再读 `control/experiments.json`、`control/tasks.json`、`docs/methods-2026-11-13-addendum.md` 和 `docs/measurement-t16-production-contract.md`。所有文件是**历史观察与方法知识**，不是生产授权；行动前必须实时读取 Shopify/Google Ads/推荐仓库。

- 2026-11-11 的“推荐技术仓库只读、不允许上线”是**历史禁令**；后续已**明确授权并完成** T16 **仅推荐曝光采集**发布。MAIN `191909396758`，可信起点 `2026-11-13T01:18:39Z`；推荐排序 `publishing_enabled=false`、反馈 `enabled=false`、质量批准 `quality_approved=false`。T16 授权不能外推为排名调整/自动学习/改动其他资源。
- T22 两条 G2 促销 RSA `831439588688`/`831439627169` 已精确启用；Script `12708189` 截止 `2026-11-30T23:00:00Z`、每日 20–21 America/Santiago；**到期真实停用仍待事后验证**，不是永久新广告授权。
- T24-D 仅将现有 Negro 变体 `51641609355542` 发布到 Online Store `313209422102`，不批准其 Shop/POS/Google & YouTube 的发布。父商品 ACTIVE 与变体 `availableForSale` 不等于变体渠道已发布。
- T24-B 4 次 Shopify/GA4 加购事件与 2 次 checkout 访问是未隔离 QA，不等于购买；T24-E 的 1 CLP 展示/Checkout 价格差**尚未修复**。
- 2026-11-12/13 智利业务日存在多个干预，均不是已验证的单变量完整日。禁止用高 Search Partners CTR、`human` 标记或 Google 无效点击数字作欺诈/购买因果结论。
- 不将 T16 的 PostHog 推荐事件与 GA4/Shopify/Ads 按未经证明的共同身份作事件级 JOIN。真实非测试消费者付款订单和扣除实际成本后的贡献利润依然是核心经营目标。

**历史记录规则**：下面保留 11/11 的旧状态与安全经验，但具体“当前状态/授权”以本段与实时平台验证为准，不能以旧快照恢复过期禁令或启动新任务。
<!-- /T26 2026-11-13 -->


<!-- growth-day-audit-2026-11-11:start -->
## ⚠ 入口优先级：活跃实验与今天已证实的反例

**所有新任务开始时**先读 `control/README.md`、`control/experiments.json`、`control/tasks.json`、`records/daily/2026-11-11-full-review.md`、`state/guards-2026-11-11-addendum.json`，再按原 `AGENTS.md` 的领域口径/来源验证/审批流程执行。

- 市场仓库是 **historical/advisory control index**，真实 Google Ads/Shopify/API 最新状态需单独读回；不能把 Git JSON 当成授权。
- PMax Purchase-only 实验起点 2026-11-11 05:12:28 America/Santiago；变更影响顾客页面、推荐集合或 Pixel 时检查实验冲突与独立用户审批。300 CNY/14 天为人工复核条件，绝非自动停投。
- **2026-11-11 历史禁令（后续 T16 有限发布授权已取代其部分范围）** `hding12/maxsensual-recs`：允许只读参照，禁止提交、触发 Actions、启用发布或修改调度，除非用户另行明确授权。
- T08 “集合页 App Pixel 不会发 ATC”已被生产数据否定。**先列全所有标准电子商务事件发送者，再提任何补发方案**。Custom Pixel v5 部署失败且已由执行 Agent 报告精确回滚，禁止以旧授权重试。
- 生产发布后 hash 未匹配授权的**预定义比较表示**时，立刻停止/回滚，不得事后自行放宽；T08 的时钟记录有冲突，只保留为有争议的 Agent 报告。
- 4 笔历史 PAID 单均经用户确认是测试，真实消费者订单/收入当时为 0；Shopify session-with-cart ≠ GA4 ATC event ≠ Ads conversion。
- 今日完整操作参见 `records/runs/2026-11-11-operations-addendum.jsonl`；从构想→审批→执行→验证→回滚严格分层。
<!-- growth-day-audit-2026-11-11:end -->

## 1. 数据口径原则

- Shopify Analytics、GA4、Google Ads 使用不同的数据模型，不得直接混用统计结果。
- Session、Visitor、Event、Product、Checkout、Payment Attempt、Order 是不同统计单位。
- 比较指标前必须确认数据源、时间范围、时区、过滤条件及分母一致。
- 比率应由对应统计范围内的总分子和总分母计算，不得直接平均各日比率。
- `human_or_bot_session = 'human'` 是 Shopify 的流量分类，不保证所有会话均为真实人工购买行为。
- 统计结果一致不代表事件定义一致；统计结果不一致也不必然代表数据采集故障。
- 不同平台的日期统计必须使用明确的店铺时区、广告账户时区或 GA4 属性时区，不得默认认为时区一致。
- 跨系统关联必须有明确的关联标识或可验证的归因依据，不得仅凭数量相同建立关联。

## 2. Shopify Session 指标定义

| 字段 | 定义及统计口径 |
|---|---|
| `sessions` | 网站访问会话数，不是独立访客数 |
| `online_store_visitors` | 去重访客数；跨日期不能直接求和 |
| `pageviews` | 会话中的页面浏览总次数 |
| `pageviews_per_session` | `pageviews / sessions` |
| `bounce_rate` | 仅产生一次页面浏览的会话数 ÷ Sessions；不等于无交互 |
| `sessions_with_cart_additions` | 至少发生一次加购的会话数，不是加购事件次数 |
| `added_to_cart_rate` | `sessions_with_cart_additions / sessions` |
| `sessions_that_reached_checkout` | 到达结账的会话数，不是支付尝试数 |
| `reached_checkout_rate` | `sessions_that_reached_checkout / sessions` |
| `sessions_that_completed_checkout` | 完成购买的会话数，不等于订单数 |
| `checkout_conversion_rate` | 完成结账会话数 ÷ 到达结账会话数 |
| `conversion_rate` | 完成结账会话数 ÷ Sessions |
| `completed_checkout_rate` | 同一会话按加购→到达结账→完成购买顺序推进的条件转化率；分母为完成前两步的会话 |
| `num_orders` | 会话产生的订单总数，统计单位为订单 |

补充原则：

- GA4 `eventCount`、`totalUsers`、`sessions` 分别对应事件、用户和会话统计单位，不得互换。
- GA4 按事件名称分组时，事件次数、用户数和发生事件的会话数必须分别解释。
- Shopify Session 指标与 GA4 Event 指标不能直接构造一一对应的事件覆盖率，除非已验证两者的统计条件及关联关系。
- 计算转化率时，应使用相同过滤条件下的分子和分母。
- 小样本的单日比率容易波动，应同时展示 Sessions 和实际行为数量。

## 3. 商品行为与着陆页

- `landing_page_path`：会话首个访问页面的路径。
- `landing_page_type`：会话首个页面的类型。
- `landing_page_type = 'Product'`：仅包含直接从商品详情页进入的会话。
- `session_viewed_product = true`：会话中记录过商品详情页浏览，不要求商品页是首个页面。
- `session_viewed_product = false`：未记录到商品详情页浏览，不等于未发生商品相关行为。
- `products_viewed`：各会话内不同商品浏览数量的汇总，不是商品页面浏览次数。
- `products_added_to_cart`：各会话内不同加购商品数量的汇总，不是加购事件次数或商品件数。
- `products_in_started_checkouts`：各会话内开始结账时所含不同商品数量的汇总。
- 按 `landing_page_path` 分组的行为指标，反映**以该页面为入口的整段会话行为**。
- 着陆页 A 归属的加购、结账或购买，不代表行为针对页面 A 对应商品。
- F03 统计所有类型的着陆页；F04 仅统计商品详情页作为入口的会话。
- F04 商品着陆页转化不等于商品自身的浏览→加购→购买转化漏斗。
- 不得通过取消 F04 的商品页入口筛选来使其结账数与全站指标相等。
- 商品详情页浏览、商品卡片曝光、商品列表浏览和商品加购是不同的行为，不得混用。

## 4. 购买路径语义

- Shopify 支持在商品详情页之外直接加购。
- Shopify Cart Permalink 可以预装商品，并直接进入购物车或结账。
- MaxSensual 已实测存在集合页快捷加购及通过 `Comprar` 永久链接进入结账的路径。
- 快捷加购可以不产生商品详情页浏览事件。
- 购物车永久链接可以在未访问商品详情页的情况下触发加购及开始结账行为。
- 商品浏览、加购、开始结账不保证在所有购买路径中严格按传统漏斗顺序发生。
- 不得假设每个加购或结账会话都必须先经过 `/products/...`。
- 购买路径的存在已得到实测支持，不代表已确定历史会话中各路径的使用比例。
- 具体按钮、链接和主题实现属于可变配置；分析当前站点时须重新核对已发布主题。

当前已验证的购买路径：

| 路径 | 用户操作 | 已观察到的行为 |
|---|---|---|
| A | 集合页 `Agregar al carrito` | 集合页快捷加购，不访问商品详情页，可触发 Shopify 原生加购事件 |
| B | 集合页 `Comprar` | 通过 Cart Permalink 预装商品并直接进入 Checkout，不要求先访问商品详情页 |
| C | 商品详情页加购 | 商品详情页浏览后加购，可产生商品浏览和加购事件 |

- 上述结果是受控浏览器测试中的实际行为，不代表所有设备、主题版本及浏览器环境均完全一致。
- 路径 B 中加购与开始结账事件的上报时间可能非常接近，不得仅凭时间相近判断用户操作顺序。
- 判断购买路径时应同时检查用户操作、购物车请求、Shopify 原生事件及 GA4 上报。

## 5. 行为时长

- `average_session_duration`：平均会话持续时间。
- `time_to_first_cart`：从会话开始到首次加购的平均时长。
- `time_to_first_checkout`：从会话开始到首次开始结账的平均时长。
- 首次行为时长只对发生相应行为的会话有意义。
- 不得将两个首次行为平均时长相减，解释为两个步骤之间的平均耗时。
- 两项首次行为时长相近，不足以证明事件同时发生。
- 上述时长不是单个商品页或着陆页的停留时长。
- 不同事件的平均时长可能来自不同会话集合，必须先确认样本范围。

## 6. 来源与归因

### Shopify 来源字段

- `traffic_type`：Shopify 对 Direct、Paid、Organic、Unknown 等流量的分类。
- `referrer_source`：推荐来源类型；Unknown 不代表完全没有 Referrer 数据。
- `referring_channel`：Shopify 识别的推荐渠道。
- `referrer_domain`：可识别的推荐域名。
- `marketing_channel`：Shopify 识别的营销渠道。
- `marketing_platform`：Shopify 归属的营销平台。
- `utm_source`、`utm_medium`、`utm_campaign`、`utm_content`、`utm_term`：分别描述来源、媒介、活动、内容及关键词标识。
- UTM 缺失不等于 Direct，也不证明流量无效。
- `session_device_browser` 是浏览器环境，不是广告来源。
- Facebook、Instagram 内置浏览器不能直接等同于 Meta Ads 来源。
- 推荐域名、渠道分类、营销平台、UTM、浏览器应作为不同维度分析。
- 不得仅凭 Referrer 或浏览器推断具体广告 Campaign。

### GA4 来源字段

- `sessionSourceMedium`：GA4 会话级来源与媒介。
- `sessionDefaultChannelGrouping`：GA4 根据来源、媒介及渠道规则进行的默认渠道分组。
- `Cross-network`：GA4 默认渠道分类之一，不等于某个具体 Referrer 域名或 Google Ads Search Partners。
- `Unassigned`：无法匹配 GA4 默认渠道分组规则的流量，不等于没有来源。
- `(not set)`：对应维度没有可用值，不等于 `Unassigned`。
- GA4 事件级来源、会话级来源及用户级来源应按各自作用域解释。

### 跨平台来源对账

- Shopify `referrer_domain`、`traffic_type` 与 GA4 `sessionSourceMedium`、`sessionDefaultChannelGrouping` 使用不同的归因模型，不能直接视为同一维度。
- GA4 `Cross-network` 不等于 Shopify 的 `syndicatedsearch.goog`，也不等于 Google Ads 的 `Search partners` 网络。
- `syndicatedsearch.goog` 是 Google 搜索广告相关服务使用的域名；不能仅凭该 Referrer 断定某次访问来自具体 Search Partners Campaign。
- Google Ads 的 `Clicks`、Shopify `Sessions`、GA4 `Sessions` 使用不同统计单位，不保证一一对应。
- 不得仅因 Shopify 与 GA4 某两个分组的 Session 数量相同，就认定它们是同一批会话。
- 比较跨平台流量时，必须明确各自的时间范围、时区、过滤条件、归因模型及分类维度。
- 自动标记、UTM 和 Referrer 是不同的归因信息来源。缺少 UTM 不代表自动标记失效。
- Google Ads 的 Campaign、广告网络、点击和花费应优先使用广告平台原生数据核对，不得单凭 Shopify Referrer 推断投放结构。

### 广告转化与收入

- Google Ads `Conversions` 与 `All conversions` 是不同统计口径。
- 必须检查 Conversion Actions、Primary/Secondary 设置及 Campaign 转化目标，才能解释广告优化方向。
- Google Ads 的 Conversion Value 不自动等于 Shopify 已实现销售收入。
- `Add to cart`、`Begin checkout`、`Purchase` 是不同转化目标，不得混合解释。
- 计算真实 ROAS 时，应使用经过核实的销售收入及可比广告花费。
- 跨平台计算金额指标前，必须核对 Google Ads 账户币种、Shopify 店铺币种及必要的汇率转换。
- 高 CTR、低 CPC、高页面事件密度或高结账到达率只能作为调查线索，不足以单独证明流量质量高低或存在自动化行为。

## 7. 事件语义与顺序

### Shopify Standard Events

- `page_viewed`：页面浏览事件。
- `collection_viewed`：集合页浏览事件。
- `product_viewed`：商品详情页浏览事件。
- `product_added_to_cart`：商品加入购物车事件。
- `checkout_started`：进入结账流程事件。
- Shopify 标准事件与 GA4 事件不存在默认的一一对应关系。

### GA4 与自定义事件

- `page_view`、`view_item`、`view_item_list`、`select_item`、`add_to_cart`、`begin_checkout`、`add_payment_info`、`purchase` 是 GA4 风格的事件名称。
- `checkout_step`、`checkout_page_view`、`msx_page`、`msx_impression` 等属于 MaxSensual 自定义事件，不等于 Shopify 标准事件。
- Shopify、GA4、Google & YouTube App Pixel、自定义 Pixel 可能分别产生、转换和发送事件。
- 不得仅凭事件名称相似认定语义、触发条件或计数口径相同。
- 必须区分用户操作、Shopify 原生事件、GA4 请求发送及 GA4 数据报告接收四个层级。
- Shopify Analytics 记录的加购或结账会话，不保证一定存在对应的 Shopify Standard Event 或 GA4 电商事件。
- 购物车请求成功，不自动证明 Shopify Pixel 或 GA4 对应事件已经触发。
- 页面事件和商品列表事件正常，不代表加购及结账事件一定正常。

### 当前 Custom Checkout Pixel 的已验证实现边界

- 自定义 `checkout_step` 使用 `msx_vid` 作为 GA4 请求的 `cid`，并携带自定义 `msx_sid`。
- `msx_sid` 是 MaxSensual 自定义会话标识，不等于 GA4 `session_id`。
- 自定义 `checkout_page_view` 使用独立的 `cid`，不保证与标准 GA4 会话身份一致。
- 自定义 Checkout 请求缺少标准 GA4 `sid`，不能默认与标准 GA4 Session 关联。
- 自定义事件可能被 GA4 接收，但其 Session Source、Page Location 和渠道归因可能不可靠。
- 补充 `page_path` 不等于修复 GA4 Client ID、Session ID 或来源归因。
- 当前已部署的自定义 Pixel V2 不再发送原始 `checkout_token`，`checkout_page_view` 的 `page_path` 固定为 `/checkout`。
- 上述内容属于当前已验证的实现状态；代码或配置变化后必须重新核实。

### 事件顺序判定

- `event.id` 是 Shopify 事件标识符；不得通过十六进制大小推断真实事件顺序。
- 判断 Shopify 原生事件顺序，应结合 `event.timestamp`、`event.seq`、客户端标识和网络捕获时间。
- GA4 `/g/collect` 的 `_p` 不得作为可靠的事件发送时间戳。
- 多条 GA4 命中具有相同 `_p`，不能证明它们同时发生、严格同序或属于同一个 HTTP 请求。
- 必须区分用户操作时间、事件产生时间、浏览器发送时间与服务端接收时间。
- 网络上行捕获顺序不必然等于用户行为真实发生顺序。
- 缺少原生时间戳或序列证据时，不得宣称已经证明严格事件顺序。

### 重复事件与 Purchase

- 同一业务行为可能由 Shopify 标准 Pixel、Google & YouTube App Pixel 和自定义 Pixel 多条链路上报。
- 必须检查各链路是否产生同名事件，以及是否存在重复计数。
- GA4 Web 数据流支持依据有效 `transaction_id` 进行购买事件去重，但不得假设不同上报链路一定已经正确去重。
- 必须核对 `transaction_id` 是否存在、是否非空、是否对应同一真实订单。
- 不得仅凭代码中存在 `purchase` 发送函数，就认定生产环境的真实 Purchase 链路已经完成端到端验证。
- 当前自定义 Purchase 与标准 Purchase 存在结构上的双链路；生产重复计数情况必须通过实际数据核实。
- 当前自定义 Purchase 的 `items` 字段只发送商品数量，不等于完整 GA4 `items[]` 商品数组。

## 8. 结账、弃单与支付

- Shopify Analytics 的到达结账会话、Shopify `checkout_started` 标准事件、Admin Abandoned Checkout 记录及 Payment Attempt 不属于同一统计单位。
- Shopify Admin API 的 Abandoned Checkout 以已提供联系方式但未完成购买的结账为基础，不覆盖所有打开结账页后离开的访问。
- 进入 Checkout 不保证立即生成 Abandoned Checkout 记录。
- Abandoned Checkout 的生成涉及联系方式提交条件及平台判定时间。
- Shopify 官方弃单判定涉及约 10 分钟的未完成结账条件；本店一次有效邮箱受控测试在联系方式提交后 625 秒（10 分 25 秒）生成弃单。
- 上述 10 分 25 秒是单次实测结果，不代表所有弃单都会在该固定时间生成。
- 少于 10 分钟的观察窗口没有查到弃单，不能据此判定生成机制故障。
- 自定义 `contact_info_submitted` 事件不等于 Shopify 已成功持久化有效联系方式。
- 应区分输入邮箱、提交表单、原生事件触发与后台联系方式保存。
- 使用无效或保留测试域名的邮箱，不能直接替代真实有效邮箱的弃单验证。
- 弃单记录的创建时间不等于用户首次进入 Checkout 的时间，也不一定等于联系方式提交时间。
- 弃单记录与进入结账会话可能跨越不同统计日期，不得直接按同日数量相减解释为联系方式提交前的流失。
- Abandoned Checkout 的 `shippingAddress` 或 `billingAddress` 为空，不足以单独证明用户未填写过地址。
- 一次有效联系方式测试成功生成弃单，只能证明该测试路径正常，不能直接估算历史结账会话的联系方式提交率。
- Payment Attempts 反映已记录的支付尝试；零支付尝试不能单独证明支付网关故障。
- 未生成订单不等于未进入结账。
- 不得直接以 Analytics Checkout Sessions ÷ Admin Abandoned Checkouts 构造转化率。

## 9. ShopifyQL 数据集边界

| 数据集 | 主要用途 |
|---|---|
| `sessions` | 会话、流量、着陆页、浏览行为及转化漏斗 |
| `web_performance` | 页面加载、交互响应及视觉稳定性 |
| `payment_attempts` | 支付尝试、成功、失败及授权 |
| `sales` | 订单与销售结果 |

- 不同数据集的指标不能默认在一条 ShopifyQL 中直接关联。
- 不得把商品浏览汇总数直接当作商品曝光次数或点击事件次数。
- 对多个数据集进行对账前，应先统一时间、过滤条件及统计单位。
- 单张 Shopify Report 保存一套查询配置；Controls 可调整当前筛选、维度和指标，但不代表支持多个独立命名视图。
- Shopify `sales` 中的订单数、Session 中的完成结账会话数和 Admin API 的订单记录不能默认视为同一统计单位。
- Shopify Order 的 Customer Journey 和 Order Attribution 可以提供来源线索，但不能证明所有未被记录的历史广告接触。
- 不同数据集的时间归属可能不同；订单创建日期、会话日期、弃单创建日期和支付尝试日期必须分别处理。

## 10. Agent 分析约束

1. 优先使用 Shopify 官方指标定义；不得自行改变原始字段语义或分母。
2. 严格区分 `VERIFIED`、`OBSERVED`、`HYPOTHESIS`、`INCONCLUSIVE` 和 `REJECTED`。
3. 单次路径测试可以证明某机制存在，不能推断历史总体中的使用比例。
4. 不将页面入口贡献解释为具体商品贡献。
5. 不将高加购率、高结账到达率直接解释为真实购买意图或优质流量。
6. 发现差异时，优先检查统计单位、事件触发条件、购买路径、过滤条件及采集时序。
7. 不能将事件关联或时间接近直接解释为因果关系。
8. 跨系统验证必须说明使用的是原生事件、转换事件还是自定义事件。
9. 测试流量须使用可识别标记；排除前验证标记确实被目标分析系统记录。
10. 本文件仅保存稳定指标语义、已验证机制及分析约束，不保存实时数值、Baseline、测试日志或临时假设。
11. Shopify 官方定义或店铺实现变化时，重新核实并更新对应条目；不得沿用过时解释。
12. 未经授权不得修改主题、Pixel、广告配置或已保存报表。
13. 必须区分 Shopify 平台测试订单和商家为诊断支付、结账等问题而进行的人工真实支付测试。
14. `test = false`、`PAID` 或 `fullyPaid = true` 只证明相应的平台订单及支付状态，不自动证明其属于真实消费者购买需求。
15. 经独立证据确认的人工测试订单，不得计入正常消费者成交、广告销售增长或盈利评估；同时应保留其财务对账记录。
16. 排除测试流量或测试订单时，应保存可验证的识别依据，不得仅凭 Direct、低金额或异常行为自行排除。
17. Shopify Customer Journey 归因为 Direct，不等于能证明用户在所有未被追踪的渠道中从未接触过广告。
18. 测试订单、真实订单、平台测试订单及支付成功状态必须分别记录，不得仅依据订单金额或财务状态分类。
19. 测试流量与真实流量混合时，必须注明数据污染范围；不能在无法确认历史测试标记时擅自重建纯真实用户统计。
20. GA4 与 Shopify 的历史数据差异，应区分事件未触发、网络未发送、身份未关联、报告处理延迟、归因分类差异及统计口径差异，不得将其中某项直接认定为唯一原因。
21. 分析 GA4 事件缺失时，应分别检查业务行为、Shopify 原生事件、浏览器请求和 GA4 报告结果，不得将它们合并为一个漏斗步骤。
22. 不能仅凭 GA4 有页面浏览事件就认定所有电商事件均已正常发送。
23. 不能仅凭 Shopify 有加购或结账记录就认定对应 GA4 事件必然已经触发。
24. 单次 Consent 对照测试只能验证相应测试环境中的隐私门控行为，不能直接推断历史用户的同意状态。
25. 对广告自动化、机器人、低质流量等判断必须提供多项独立证据，不得仅凭高事件密度、高 CTR 或异常转化率下结论。

## 11. 数据安全与 Customer Privacy

### 敏感数据保护

- 不得将原始 Checkout Token、客户邮箱、电话、地址、Cookie 或其他敏感标识发送到分析平台的自定义事件参数。
- 检查数据泄露时，必须检查事件参数值、URL 路径、查询参数、页面位置和 Referrer；仅检查敏感字段名称是否存在是不充分的。
- 不得将原始 Checkout Token 放入 `page_path`、`page_location`、`page_referrer`、`checkout_url` 或其他自定义参数。
- 对 Checkout URL 及网络抓包进行分析或归档时，应采用脱敏路径，避免在报告、日志和代码审查记录中暴露原始 Token。
- 不得通过简单哈希或截断方式将原始敏感标识变成长期可关联的分析标识，并默认认为其已经匿名化。
- 诊断事件只应发送完成分析所必需的字段。
- GA4、Google Ads 等外部分析平台不得作为保存原始 Checkout Token 或客户敏感信息的业务数据库。

### Customer Privacy

- Shopify Customer Events 的平台隐私门控、Pixel 代码中的主动 Consent 检查，以及 GA4 请求中的 Consent 参数属于不同层级。
- Shopify 可以根据 Custom Pixel 的 Privacy 设置控制 Pixel 的执行权限。
- Pixel 代码没有主动调用 `customerPrivacy` 或 `consent` API，不等于平台没有执行隐私门控。
- 缺少 `gcs` 或 `gcd` 不足以单独证明未经同意采集。
- 必须分别检查后台 Privacy 配置、运行时授权状态及实际网络请求。
- Shopify Custom Pixel 的隐私配置可能变化；分析当前行为前应重新核实。
- 不得通过硬编码 `gcs`、`gcd` 或其他 Consent 参数模拟用户授权。
- 未经明确授权不得修改 Customer Privacy、Analytics Consent 或 Marketing Consent 配置。

### 当前已知的 Token 外发边界

- 当前已部署的自定义 Checkout Pixel V2 已移除原始 `checkout_token` 外发。
- 当前自定义 `checkout_page_view` 使用固定 `page_path = '/checkout'`。
- 最近一次真实抓包仍观察到 Shopify Google & YouTube 标准 GA4 `page_view` 和 `begin_checkout` 的 `dl` 包含 Checkout URL 路径中的 Token。
- 上述标准 GA4 Token 外发属于独立链路，不得因为自定义 Pixel 已修复就宣称全站不存在 Token 外发。
- 标准 Google & YouTube Pixel 的处理必须单独审计，未经授权不得修改。

## 12. Pixel 部署与配置变更约束

- Shopify Custom Pixel 编辑器接受的代码层级必须与实际编辑器格式一致，不得将完整沙箱渲染包装代码直接写入只接受内层源码的编辑器。
- 修改 Pixel 前必须读取当前实际线上代码，不得只依赖本地备份。
- 文件校验必须比较相同层级的源码，不得将内层代码与完整包装脚本的 SHA-256 直接比较。
- 发布前必须核对代码结构，确认不存在重复包装或意外嵌套。
- 保存后必须重新读取编辑器内容，并检查实际部署结构。
- 不得仅凭 SHA-256 一致就认定部署成功。
- 每次部署后必须立即执行真实浏览器网络冒烟测试，确认关键事件仍正常发送。
- 应检查自定义事件、标准 GA4 事件、敏感参数、JavaScript 错误及 Pixel 状态。
- 回滚版本必须保存安全的内层源码，不得直接恢复存在已知敏感数据泄露问题的历史版本。
- 如果新版本发生故障，应优先停发或修复受影响的自定义事件，不得为了恢复数据而重新引入原始 Token 外发。
- 变更范围必须明确，不得在修复一个 Pixel 问题时顺带修改 GA4、Google Ads、主题或 Customer Privacy。
- 未经用户明确授权，不得部署 Pixel、修改主题、调整 GA4、修改 Google Ads 或更改已保存报表。
- 每次部署必须记录版本标识、修改范围、验证结果、故障窗口及回滚方案。
