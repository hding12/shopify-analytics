#!/usr/bin/env python3
"""Validate the 2026-11-13 knowledge addendum (offline, read-only).

This validates documentation/provenance integrity only. It does not verify live
Shopify/Google Ads state, automatically authorize writes or redact full API dumps.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-11-13"
RELEASE_FILES = [
    "docs/methods-2026-11-13-addendum.md",
    "docs/measurement-t16-production-contract.md",
    "records/daily/2026-11-12-t20-t22-promo-rsa.md",
    "records/daily/2026-11-13-t16-t25-growth-review.md",
    "state/guards-2026-11-13-addendum.json",
    "records/decisions/2026-11-13-addendum.json",
    "records/insights/2026-11-13-addendum.json",
    "records/runs/2026-11-12-to-13-operations.jsonl",
]
SOURCE_KINDS = {
    "user_agent_report", "direct_platform_raw_api", "connector_readback",
    "browser_observation", "model_derived"
}
EXECUTION_STATES = {
    "PROPOSED", "APPROVED", "EXECUTED", "READBACK_VERIFIED",
    "BLOCKED", "ROLLED_BACK"
}
INSIGHT_STATES = {
    "HYPOTHESIS", "OBSERVED", "VERIFIED", "INCONCLUSIVE",
    "REJECTED", "SUPERSEDED"
}
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
TOKEN_RE = re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._-]{18,}|shpat_[A-Za-z0-9]{16,}|xox[baprs]-[A-Za-z0-9-]{16,})")
CHECKOUT_RE = re.compile(r"https?://\S*(?:checkout|checkouts)/\S*(?:token=|key=|[a-f0-9]{32})", re.I)


def fail(msg: str) -> None:
    raise ValueError(msg)


def unique_pairs(items):
    result = {}
    for k, v in items:
        if k in result:
            fail(f"duplicate JSON property {k}")
        result[k] = v
    return result


def read_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)


def read_jsonl(rel: str):
    text = (ROOT / rel).read_text(encoding="utf-8")
    return [json.loads(line, object_pairs_hook=unique_pairs) for line in text.splitlines() if line.strip()]


def aware(s: str | None) -> bool:
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.tzinfo is not None and dt.utcoffset() is not None
    except (TypeError, ValueError, AttributeError):
        return False


def safe_public_text(s: str) -> bool:
    return not (EMAIL_RE.search(s) or TOKEN_RE.search(s) or CHECKOUT_RE.search(s))


def ensure_public_safe(text: str, path: str) -> None:
    if not safe_public_text(text):
        fail(f"Potential private email/token/checkout URL in {path}; redact before public push")


def unique_rows(rows, key: str, label: str) -> set[str]:
    ids = [obj.get(key) for obj in rows]
    if not ids or not all(isinstance(i, str) and i for i in ids) or len(ids) != len(set(ids)):
        fail(f"Missing/duplicate {key} in {label}")
    return set(ids)


def validate() -> str:
    for p in RELEASE_FILES:
        if not (ROOT / p).is_file():
            fail(f"Missing artifact {p}")
        ensure_public_safe((ROOT / p).read_text(encoding="utf-8"), p)

    portfolio, experiments, tasks = [read_json(p) for p in (
        "control/portfolio.json", "control/experiments.json", "control/tasks.json"
    )]
    dates = [portfolio.get("snapshot_as_of_date"), experiments.get("as_of_date"), tasks.get("as_of_date")]
    if dates != [STAMP] * 3:
        fail(f"Control snapshots must all be {STAMP}, got {dates}")
    if portfolio.get("state_policy") != "HISTORICAL_OBSERVATION_NOT_LIVE_AUTHORITY":
        fail("Control snapshot must not masquerade as live system or authorization")
    modules = {m.get("id"): m for m in portfolio.get("modules", [])}
    rec = modules.get("recommendations", {})
    if rec.get("capture_status_at_snapshot") != "PRODUCTION_CAPTURE_ONLY_PASS":
        fail("T16 capture must be distinct from ranking and have validated production status")
    if rec.get("publishing_enabled_at_snapshot") is not False or rec.get("feedback_learning_enabled_at_snapshot") is not False:
        fail("Ranking/feedback must remain disabled")
    if rec.get("trusted_capture_start_utc") != "2026-11-13T01:18:39Z":
        fail("T16 trusted capture start must not be the theme publish time")

    exps = experiments.get("experiments", [])
    exp_ids = unique_rows(exps, "id", "control/experiments")
    if "EXP-G2-PROMO-RSA-20261112" not in exp_ids:
        fail("Missing T22 monitored promotion experiment")
    pmax = next((x for x in exps if x["id"] == "EXP-PMAX-PURCHASE-ONLY-20261111"), None)
    if not pmax or pmax.get("first_clean_business_day") is not None:
        fail("Cannot label a contaminated 11/13 CL business day as clean")
    if pmax.get("review", {}).get("mode") != "FIRST_OF_MANUAL_REVIEW_NOT_AUTOMATIC_PAUSE":
        fail("PMax must retain manual, not automatic spending review")
    if pmax["review"]["after_incremental_spend"].get("hard_cap") is not False:
        fail("300 CNY PMax review is not a hard budget cap")
    for e in exps:
        if e["id"] == "EXP-G2-PROMO-RSA-20261112":
            targets = sorted(e["review"]["ad_ids"])
            if targets != ["831439588688", "831439627169"] or e["review"]["script_id"] != "12708189":
                fail("Promo whitelist drift")
            if e["review"]["script_cutoff_utc"] != "2026-11-30T23:00:00Z":
                fail("Promo script UTC cutoff drift")

    guards = read_json("state/guards-2026-11-13-addendum.json")
    if guards.get("classification") != "PUBLIC_HISTORICAL_SNAPSHOT_NOT_LIVE_PERMISSION":
        fail("Guards must be historical observation, never standing authority")
    g = guards.get("constraints", [])
    guard_ids = unique_rows(g, "id", "guards")
    if len(guard_ids) < 10 or any(x.get("live_readback_required") is not True or x.get("historical_only") is not True for x in g):
        fail("All guards must require live readback and be historical-only")

    insights = read_json("records/insights/2026-11-13-addendum.json")
    insight_ids = unique_rows(insights, "id", "insights")
    if len(insight_ids) < 8:
        fail("Too few insight records")
    for x in insights:
        if x.get("status") not in INSIGHT_STATES or not aware(x.get("observed_at")):
            fail(f"Bad insight state/time: {x.get('id')}")
        if not x.get("sources") or not x.get("limitations") or x.get("visibility") != "public":
            fail(f"Missing source/limitations or wrong visibility for {x['id']}")
    decisions = read_json("records/decisions/2026-11-13-addendum.json")
    decision_ids = unique_rows(decisions, "id", "decisions")
    for x in decisions:
        if x.get("implementation_status") not in EXECUTION_STATES:
            fail(f"Bad decision implementation status: {x['id']}")
        if x.get("standing_production_authorization") is not False:
            fail(f"Public decision grants invalid production approval: {x['id']}")
        if any(ref not in insight_ids for ref in x.get("related_insights", [])):
            fail(f"Dangling insight ref in {x['id']}")

    events = read_jsonl("records/runs/2026-11-12-to-13-operations.jsonl")
    event_ids = unique_rows(events, "event_id", "operations")
    if len(event_ids) < 10:
        fail("Too few operation records")
    for x in events:
        if x.get("execution_status") not in EXECUTION_STATES or x.get("source_kind") not in SOURCE_KINDS:
            fail(f"Bad event state/source: {x['event_id']}")
        if x.get("occurred_at") is not None and not aware(x["occurred_at"]):
            fail(f"Invalid or timezone-naive exact action time: {x['event_id']}")
        if x.get("standing_authorization") is not False:
            fail(f"Event grants standing write authorization: {x['event_id']}")
        if not x.get("verification") or not isinstance(x.get("target"), dict) or not x.get("evidence_refs"):
            fail(f"Missing target/verification/evidence: {x['event_id']}")
    proposed = next((x for x in events if x["event_id"] == "RUN-T26-T24E-PRICE"), None)
    if not proposed or proposed["execution_status"] != "PROPOSED" or not proposed["verification"].get("not_deployed"):
        fail("T24-E must remain proposed, not falsely logged as a deployment")

    # Cross-release uniqueness: don't re-use ID of older records.
    for collection, glob, key, new_ids in [
        ("insights", "records/insights/*.json", "id", insight_ids),
        ("decisions", "records/decisions/*.json", "id", decision_ids),
    ]:
        for f in ROOT.glob(glob):
            if f.name.startswith("2026-11-13-"):
                continue
            val = read_json(str(f.relative_to(ROOT)))
            if isinstance(val, list) and new_ids.intersection(x.get(key) for x in val if isinstance(x, dict)):
                fail(f"Duplicate {collection} IDs with existing file: {f}")
    for f in (ROOT / "records/runs").glob("*.jsonl"):
        if f.name == "2026-11-12-to-13-operations.jsonl":
            continue
        try:
            old = read_jsonl(str(f.relative_to(ROOT)))
        except json.JSONDecodeError:
            fail(f"Invalid historical operations JSONL: {f}")
        if event_ids.intersection(x.get("event_id") for x in old if isinstance(x, dict)):
            fail(f"Duplicate operation IDs with prior log: {f}")
    if "T26 2026-11-13" not in (ROOT / "AGENTS.md").read_text(encoding="utf-8"):
        fail("Agent instructions must prioritize the updated 2026-11-13 historical control index")
    return f"PASS: {len(g)} guards, {len(insights)} insights, {len(decisions)} decisions, {len(events)} actions; T16 capture-only, T22 scope, 11/13 mixed day verified as records"


if __name__ == "__main__":
    try:
        print(validate())
    except (ValueError, OSError, KeyError, TypeError, IndexError) as e:
        print("FAIL: " + str(e))
        raise SystemExit(1) from e
