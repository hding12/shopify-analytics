# Insight and decision lifecycle

A coherent history has **observations** (what happened), **insights** (bounded interpretation), **decisions** (authorized choice), and **operations** (actual platform mutations). Never collapse them into one text note.

## Insight schema essentials

`id`, `title`, `observed_at`, `window`, `timezone`, `claim_status`, `statement`, `metrics` (units + denominator), `source_refs`, `alternative_explanations`, `limitations`, `relevance`, `suggested_action`, `expires_at`, `contradicted_by` / `superseded_by`.

An `INS-...` note may be OBSERVED without being a causal claim. A data source citation must identify the exact query / API record, not merely "Shopify" or "Supermetrics".

## Decision record essentials

`id`, `date`, `problem`, `options_considered`, `decision`, `scope`, `approval_ref`, `reasoning`, `constraints_checked`, `reversibility`, `supersedes`, `related_insights`, `related_runs`, `result`.

**Decision revisions are first-class knowledge:** A traditional merchandising decision that rejects a product for negative contribution was superseded once its objective was clarified as a bounded market-discovery experiment. Preserve both decisions and the reason for the revision.

## Evidence quality

- `VERIFIED`: directly read back or independently observed under specified conditions.
- `OBSERVED`: one reliable observation, no causality/generalization.
- `INCONCLUSIVE`: missing critical measurement or confounded test.
- `REJECTED`: supported counter-evidence invalidates the earlier hypothesis.
- `SUPERSEDED`: previous decision/method is not the current operating rule.

Treat plugin heuristics (e.g., a default 3x CPA alert) as configurable triggers, not confirmed market facts.
