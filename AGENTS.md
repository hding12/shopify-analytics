# AGENTS.md — MaxSensual Analytics

## 1. 数据口径原则

- Shopify Analytics、GA4、Google Ads 使用不同的数据模型，不得直接混用统计结果。
- Session、Visitor、Event、Product、Checkout、Payment Attempt、Order 是不同统计单位。
- 比较指标前必须确认数据源、时间范围、时区、过滤条件及分母一致。
- 比率应由对应统计范围内的总分子和总分母计算，不得直接平均各日比率。
- `human_or_bot_session = 'human'` 是 Shopify 的流量分类，不保证所有会话均为真实人工购买行为。
- 统计结果一致不代表事件定义一致；统计结果不一致也不必然代表数据采集故障。

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

## 3. 商品行为与着陆页

- `landing_page_path`：会话首个访问页面的路径。
- `landing_page_type`：会话首个页面的类型。
- `landing_page_type = 'Product'`：仅包含直接从商品详情页进入的会话。
- `session_viewed_product = true`：会话中记录过商品详情页浏览，不要求商品页是首个页面。
- `session_viewed_product = false`：未记录到商品详情页浏览；不等于未发生商品相关行为。
- `products_viewed`：各会话内不同商品浏览数量的汇总，不是商品页面浏览次数。
- `products_added_to_cart`：各会话内不同加购商品数量的汇总，不是加购事件次数或商品件数。
- `products_in_started_checkouts`：各会话内开始结账时所含不同商品数量的汇总。
- 按 `landing_page_path` 分组的行为指标，反映**以该页面为入口的整段会话行为**。
- 着陆页 A 归属的加购、结账或购买，不代表行为针对页面 A 对应商品。
- F03 统计所有类型的着陆页；F04 仅统计商品详情页作为入口的会话。
- F04 商品着陆页转化不等于商品自身的浏览→加购→购买转化漏斗。
- 不得通过取消 F04 的商品页入口筛选来使其结账数与全站指标相等。

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

## 5. 行为时长

- `average_session_duration`：平均会话持续时间。
- `time_to_first_cart`：从会话开始到首次加购的平均时长。
- `time_to_first_checkout`：从会话开始到首次开始结账的平均时长。
- 首次行为时长只对发生相应行为的会话有意义。
- 不得将两个首次行为平均时长相减，解释为两个步骤之间的平均耗时。
- 两项首次行为时长相近，不足以证明事件同时发生。
- 上述时长不是单个商品页或着陆页的停留时长。

## 6. 来源与归因

- `traffic_type`：Shopify 对 Direct、Paid、Organic、Unknown 等流量的分类。
- `referrer_source`：推荐来源类型；Unknown 不代表完全没有 Referrer 数据。
- `referring_channel`：Shopify 识别的推荐渠道。
- `referrer_domain`：可识别的推荐域名。
- `marketing_platform`：Shopify 归属的营销平台。
- `utm_source`、`utm_medium`、`utm_campaign`、`utm_content`：分别描述来源、媒介、活动及内容标识。
- UTM 缺失不等于 Direct，也不证明流量无效。
- `session_device_browser` 是浏览器环境，不是广告来源。
- Facebook、Instagram 内置浏览器不能直接等同于 Meta Ads 来源。
- 推荐域名、渠道分类、营销平台、UTM、浏览器应作为不同维度分析。
- 不得仅凭 Referrer 或浏览器推断具体广告 Campaign。

## 7. 事件语义与顺序

### Shopify Standard Events

- `product_viewed`：商品详情页浏览事件。
- `product_added_to_cart`：商品加入购物车事件。
- `checkout_started`：进入结账流程事件。
- Shopify 标准事件与 GA4 事件不存在默认的一一对应关系。

### GA4 与自定义事件

- `view_item`、`add_to_cart`、`begin_checkout` 是 GA4 风格的电商事件名称。
- `checkout_step`、`checkout_page_view` 属于 MaxSensual 自定义事件，不等于 Shopify 标准事件。
- Shopify、GA4、自定义 Pixel 可能分别产生、转换和发送事件。
- 不得仅凭事件名称相似认定语义、触发条件或计数口径相同。

### 事件顺序判定

- `event.id` 是 Shopify 事件标识符；不得通过十六进制大小推断真实事件顺序。
- 判断 Shopify 原生事件顺序，应结合 `event.timestamp`、`event.seq`、客户端标识和网络捕获时间。
- GA4 `/g/collect` 的 `_p` 不得作为可靠的事件发送时间戳。
- 多条 GA4 命中具有相同 `_p`，不能证明它们同时发生、严格同序或属于同一个 HTTP 请求。
- 必须区分用户操作时间、事件产生时间、浏览器发送时间与服务端接收时间。
- 网络上行捕获顺序不必然等于用户行为真实发生顺序。
- 缺少原生时间戳或序列证据时，不得宣称已经证明严格事件顺序。

## 8. 结账、弃单与支付

- Shopify Analytics 的到达结账会话、Shopify `checkout_started` 标准事件、Admin Abandoned Checkout 记录和 Payment Attempt 不属于同一统计单位。
- Shopify Admin API 的 Abandoned Checkout 以已提供联系方式但未完成购买的结账为基础，不覆盖所有打开结账页后离开的访问。
- 进入 Checkout 不保证立即生成 Abandoned Checkout 记录。
- 自定义 `contact_info_submitted` 事件不等于 Shopify 已成功持久化有效联系方式。
- 弃单判定涉及平台条件及处理延迟；短时间查询不到记录，不足以断言不会生成弃单。
- 应区分输入邮箱、提交表单、原生事件触发与联系方式持久化。
- 使用无效或保留测试域名的邮箱，不能直接验证真实有效联系方式的弃单行为。
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