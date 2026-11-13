# MaxSensual Growth Control v1

<!-- T26 2026-11-13 -->
## 2026-11-13 快照（优先于 11/11 历史记录）

此目录只是人工决策索引，不连接生产 API，不持有授权，不替代资源锁。请先读 `../state/guards-2026-11-13-addendum.json`、新方法 `../docs/methods-2026-11-13-addendum.md` 与 `../records/daily/2026-11-13-t16-t25-growth-review.md`。

- T16 的**推荐采集**已发布至 MAIN `191909396758`，可信起点 `2026-11-13T01:18:39Z`；排序发布/反馈学习仍关闭。11/11 “推荐仓库只读”仅为历史决定。
- T22 已精确启用两条 G2 促销 RSA，并有到期 Script，执行后的新授权不自动产生。
- 11/12–13 CL 发生多次客户可见变化/QA，不能凭 `first_clean_business_day` 的老值判定纯净日。
- `check-change` 仍只给出提醒，任何输出（包括 `NO_KNOWN_CONFLICT`）都不是可写权限。
<!-- /T26 2026-11-13 -->


<!-- growth-day-audit-2026-11-11:start -->
## 2026-11-11 增量审计与当日纠错

- [当日全量回顾](../records/daily/2026-11-11-full-review.md)
- [PMax 与推荐变更保护](../state/guards-2026-11-11-addendum.json)
- [操作追溯 JSONL](../records/runs/2026-11-11-operations-addendum.jsonl)
- [T08 Pixel 回滚事故](../docs/incidents/T08-2026-11-11-production-rollback.md)

本目录仍是人工决策索引，不是实时状态同步或跨仓库强制锁。推荐技术仓库只读参照；市场主线优先真实消费者购买而非推荐 CTR 或 GA4 加购数量。
<!-- growth-day-audit-2026-11-11:end -->

**Single business-control entrypoint. No changes to the recommendation repository.**

This directory is a small, versioned coordination layer for experiments, tasks and cross-system risks. It complements `AGENTS.md`, `docs/agent-execution.md` and the existing evidence/decision records; it is **not** a new deployment system.

| File | Purpose |
|---|---|
| `portfolio.json` | Business objectives, module status and source/repository boundaries |
| `experiments.json` | Active experiments, checkpoint rules and customer-facing change guards |
| `tasks.json` | Execution backlog and the meaning of current task statuses |
| `integrations.md` | Responsibility split and approval / readback rules |

## Run locally

From the **shopify-analytics** repository root (no third-party packages):

```bash
python3 scripts/growth_control.py validate
python3 scripts/growth_control.py status
python3 scripts/growth_control.py check-change --resource shopify:collection:para-ella
```

The last command intentionally exits **2** when active business experiments require explicit approval. This is **not** an automatic Shopify/GitHub lock and does not prohibit later approved changes. In this phase no recommendation job is triggered and no Shopify write is performed.

## How to update

- Update observations after reading the real Google Ads / Shopify / GitHub source. Add the source and business date; no stale JSON field is standing approval.
- Keep each experiment's ID stable; supersede decisions rather than rewriting past incidents. Put detailed chronology into existing `records/`.
- After the PMax review, the growth lead may change its experiment state to `COMPLETED` **only based on a recorded decision**. The advisory change guard then stops matching automatically.
- Public repo: safe summary facts only. Never put API secrets, customer identity, full checkout URLs, raw payment data or unrevised evidence dumps here.

**Current status (historical snapshot):** PMax Purchase-only is active; rules_v1 recommendations passed the latest dry run but have **not** been published; earlier Custom Pixel T08 duplicate-event patch was rolled back.
