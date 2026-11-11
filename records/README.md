# Published G1/G2/G2X historical records

<!-- growth-day-audit-2026-11-11:start -->
## 2026-11-11 新增历史与纠错（不覆盖旧 G1–G2X 记录）

- [当日增量审计索引](daily/2026-11-11-full-review.md)
- [独立操作日志 21 条](runs/2026-11-11-operations-addendum.jsonl)
- [新增 8 项决策](decisions/2026-11-11-addendum.json)
- [新增 17 条洞察（含 REJECTED）](insights/2026-11-11-addendum.json)

旧有关键词政策豁免、精确否词、CPC micros、G2X、折扣冲突和 Supermetrics 方法论仍保存在此前目录中，本次不重复计入新写入操作。
<!-- growth-day-audit-2026-11-11:end -->

**Publication:** The operator expressly authorized releasing these historical business records to the public `hding12/shopify-analytics` repository on 2026-11-11. This folder was originally prepared as a private companion bundle; its designation has been superseded by this public release.

These records reconstruct events from operator/Agent reports and selected independently verified connector readings. They are **not** a complete audit trail and **do not** contain the original API request/response snapshots, screenshots, purchase logs or evidence hashes.

Contents include product IDs, Campaign and Ad Group IDs, ad budgets, estimated sourcing costs and references to an operator test payment. The package contains no intentionally included customer names, email addresses, passwords, access tokens or raw Checkout Tokens.

Evidence handling:

- Keep source type, date window, confidence, and evidence pointer on every claim.
- `occurred_at: null` means the actual event timestamp is not known; do not synthesize a precise timestamp.
- `EXECUTED` and `READBACK_VERIFIED` are different states; do not promote a report into independent verification.
- Replace unresolved evidence references with verified snapshots and SHA-256 hashes when they are available, but redact sensitive details before public commits.
- Treat all `state/constraints.yaml` fields as **historical**, not permissions that authorize a new write. Confirm live campaign state and current user authorization first.

See [`../AGENTS.md`](../AGENTS.md) for enduring data definitions and [`../docs/architecture.md`](../docs/architecture.md) for the record lifecycle.
