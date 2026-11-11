# MaxSensual Growth Control v1

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
