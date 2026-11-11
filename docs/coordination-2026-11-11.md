# 市场增长统一入口与技术仓库只读协同边界

> **当前决定：两个仓库不合并，暂时不修改/调度推荐仓库。** 本文件为市场仓库管理接口说明，不是新的远程自动化系统，也不是用户对推荐发布的授权。

## 分工

| 所属仓库 | 权威范围 | 不代表什么 |
|---|---|---|
| Public `hding12/shopify-analytics` | 增长目标、商业决策、实验保护、运营日志和脱敏证据引用 | 当前 Google/Shopify 平台 live config、技术代码发布成功、强制安全锁 |
| Private `hding12/maxsensual-recs` | 规则推荐实现、Shopify 集合发布器、PostHog 反馈和私有运行状态 | 增长实验审批、真实成交证据；不能由本仓库“自动授权” |
| Google Ads / Shopify / GA4 / PostHog live APIs | 各平台运行时状态/报告 | 不自动代替来自用户的具体授权 |

## 单向流程（当前）

1. 市场增长 Agent 读取 `AGENTS.md`、`control/`、今天增量和长期 `records/`，同时对活跃业务状态执行新的 API 读回。
2. 市场 Agent 可以**只读**推荐技术仓库 README、代码、GitHub Actions/私有状态等，识别发布计划会更换哪些商品与集合，但不能触发它的新任务。
3. 如提出跨项目生产动作，先进行影响集合/落地页扫描、明确资源/实验/时区/旧新快照，走单独用户审批。
4. 当前“执行回传”仍由人或本地 Agent 手动提供摘要和证据引用；市场仓库只保存**脱敏摘要**，私有原始技术资料留在相应私有库或本地。
5. 用户确认以后需要自动协作时再讨论拉取受版本约束的政策和 Fail-Closed 发布门禁；**不在本次改推荐库或 GitHub secrets**。

## 实验冲突样例：PMax 与 Shopify 推荐

- PMax `24244298528` 于 11/11 05:12:28 -03 修改 Purchase-only；第一完整观测日从 11/12 起。
- 推荐批量规则 `rules_v1` 有 26 个推荐位，主页 10 个产品；最新 dry run 0 blockers 但 `apply=false`、无 Shopify published records。
- 候选发布会把首页 10 件全部替换，并重排 `para-ella` 等广告可能落地集合；在同一时间变更多项因素会让净购买归因失去单变量对照。
- 市场控制文件的 `APPROVAL_REQUIRED` 不是绝对禁止发布：只有在明确说明原因、允许修改的集合和新的实验观察边界，获得另一次授权，才可考虑在未来发布。现阶段用户明确要求**不动推荐仓库**。
- 若库存严重错误需要紧急纠正，仍需精确范围和重新读回，不得借“无 publish blockers”绕过授权。

## 实用检查

```bash
python3 scripts/growth_control.py validate
python3 scripts/growth_control.py status
python3 scripts/growth_control.py check-change --resource shopify:collection:para-ella
```

该命令不会访问生产 API，也不会直接阻止外部 Agent；所有状态均带快照性质。

## 双向协作的未来验收条件（尚未实现）

- market repo 的政策 commit SHA 可引用而不会暗中改变正在执行的计划；授权包含目标集合、动作、审批人、窗口、到期时点。
- 技术库必须在准备真正 `--apply` 前强制检查活跃资源冲突，存在不明确的状态则 Fail Closed。
- 技术 Agent 返回 `plan_id`、affected placements、before/after、readback、journal、rollback verification 和 business-experiment-boundary，严格不写原始客户信息到 Public 仓库。
- 同一 Shopify 集合只能由一个发布器占有写权限；项目切换时旧调度器关闭、新运行器通过状态一致性和锁验收。
