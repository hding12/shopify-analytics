# MaxSensual · Shopify Analytics & Growth Knowledge Base

A versioned knowledge base for evidence-backed Shopify, Google Ads, GA4, Supermetrics and Agent growth operations. It separates reusable methods, current guardrails, observed market signals, business decisions, and append-only action history.

> **Publication notice (2026-11-11):** The repository is public. The operator explicitly authorized publishing both the previously public-safe methodology and the historical business records. Campaign IDs, budgets, supplier-source prices and test-order references below are intentionally published. Do not add credentials, access tokens, customer contact information, full checkout URLs or raw sensitive API payloads. History is not a substitute for current platform state.

## Read in this order

1. [`AGENTS.md`](AGENTS.md) — existing durable analytics semantics and safety constraints (preserved).
2. [`docs/architecture.md`](docs/architecture.md) — methodology, facts, constraints, decisions, actions and evidence relationship.
3. [`docs/business-model.md`](docs/business-model.md) — profit-oriented own inventory vs bounded-loss sourced-catalog demand exploration.
4. [`docs/method-catalog.md`](docs/method-catalog.md) — portable growth and data-analysis methods.
5. [`docs/supermetrics-methods.md`](docs/supermetrics-methods.md) — plugin-provided methods and application limits.
6. [`docs/analytics-application.md`](docs/analytics-application.md) — correct data-source, attribution and event interpretation.
7. [`docs/insights-and-decisions.md`](docs/insights-and-decisions.md) — claim confidence, decisions, revision and supersession.
8. [`docs/agent-execution.md`](docs/agent-execution.md) — permissions, preflight, mutations, readback and rollback.
9. [`docs/incident-lessons.md`](docs/incident-lessons.md) and [`docs/case-history-sanitized.md`](docs/case-history-sanitized.md) — failures and lessons.
10. [`records/README.md`](records/README.md) and [`records/chronology.md`](records/chronology.md) — published G1→G2→G2X historical reconstruction.

## Structured records

| Artifact | Path | Interpretation |
|---|---|---|
| Business constraints snapshot | [`state/constraints.yaml`](state/constraints.yaml) | **Historical snapshot only.** Re-query production API and confirm authority before acting. |
| Insights | [`records/insights/insights.json`](records/insights/insights.json) | Claims with explicit confidence/limits; not immutable business truths. |
| Decisions | [`records/decisions/decisions.json`](records/decisions/decisions.json) | Includes overturned AG-E NO-GO and later dual-track revision. |
| Applied plugin insights | [`records/methods-in-practice.md`](records/methods-in-practice.md) | Distinguishes Supermetrics workflows actually used from unvalidated methods. |
| Operation history | [`records/runs/2026-11-g2-g2x-reconstructed.jsonl`](records/runs/2026-11-g2-g2x-reconstructed.jsonl) | Reconstructed event summaries, not full provider audit logs. |
| Schemas | [`schemas/`](schemas/) | Validation shapes for future records. |
| Templates | [`docs/recording-template.md`](docs/recording-template.md) | Methods, constraints, insights and action log examples. |
| Roadmap | [`docs/migration-plan.md`](docs/migration-plan.md) | Follow-up CI, provenance and evidence improvements. |

## Data quality contract

- **Observed ≠ proven causal; API success ≠ readback verified; policy exemption ≠ approved ad; test payment ≠ real consumer order.**
- The latest stored budgets, dates, inventory values, discounts and ad approvals may be stale. Production APIs control the current state.
- Store operator authorization, time zone, currency, raw unit, scope, evidence source and supersession links with each decision or write.
- Raw screenshots and full platform responses referred to in the chronology are **not included** in these packages; do not fabricate hashes or timestamps.
- Never commit credentials or customer PII. Restrict future raw evidence by content rather than assuming every reconstructed business record is secret.
