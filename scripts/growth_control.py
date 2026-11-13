#!/usr/bin/env python3
"""Small, read-only growth-decision index. Never calls a production API."""
from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / "control"
ALLOWED_EXPERIMENT_STATES = {"ACTIVE", "PRELAUNCH", "PAUSED", "COMPLETED", "CANCELLED"}


class ControlError(ValueError):
    pass


def no_duplicate_keys(pairs):
    result = {}
    for key, val in pairs:
        if key in result:
            raise ControlError(f"Duplicate JSON key: {key}")
        result[key] = val
    return result


def read(name):
    path = CONTROL / name
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)
    except (OSError, json.JSONDecodeError, ControlError) as exc:
        raise ControlError(f"Cannot read {name}: {exc}") from exc


def require(cond, message):
    if not cond:
        raise ControlError(message)


def iso(timestamp):
    try:
        t = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return t.tzinfo is not None and t.utcoffset() is not None
    except (TypeError, ValueError, AttributeError):
        return False


def load_and_validate():
    portfolio = read("portfolio.json")
    experiments = read("experiments.json")
    tasks = read("tasks.json")
    for name, obj in (("portfolio", portfolio), ("experiments", experiments), ("tasks", tasks)):
        require(obj.get("schema_version") == 1, f"{name} has unsupported schema")
        require(obj.get("as_of_date", obj.get("snapshot_as_of_date", "")) == portfolio.get("snapshot_as_of_date"),
                f"{name} snapshot date mismatch")
    require(portfolio.get("control_repo") == "hding12/shopify-analytics", "Unexpected control repository")
    require(portfolio.get("business_timezone") == "America/Santiago", "Business timezone changed")
    require(portfolio.get("state_policy") == "HISTORICAL_OBSERVATION_NOT_LIVE_AUTHORITY", "Missing historical-state warning")
    mods = portfolio.get("modules")
    require(isinstance(mods, list) and mods, "Empty modules")
    module_ids = [m.get("id") for m in mods]
    require(len(module_ids) == len(set(module_ids)), "Duplicate module IDs")

    exps = experiments.get("experiments")
    require(isinstance(exps, list) and exps, "Empty experiments")
    exp_ids = [e.get("id") for e in exps]
    require(None not in exp_ids and len(set(exp_ids)) == len(exp_ids), "Duplicate/missing experiment IDs")
    for exp in exps:
        exp_id = exp["id"]
        require(exp.get("status") in ALLOWED_EXPERIMENT_STATES, f"Unknown state for {exp_id}")
        if exp.get("status") == "ACTIVE":
            require(iso(exp.get("started_at_utc")), f"Invalid UTC start for {exp_id}")
            require(iso(exp.get("started_at_local")), f"Invalid local start for {exp_id}")
            guard = exp.get("change_guard", {})
            require(guard.get("mode") == "APPROVAL_REQUIRED", f"Active experiment has no explicit change guard: {exp_id}")
            patterns = guard.get("resource_patterns")
            require(isinstance(patterns, list) and patterns and all(isinstance(p, str) and ":" in p for p in patterns),
                    f"Invalid protected resource patterns: {exp_id}")
            review = exp.get("review", {})
            mode = review.get("mode")
            if mode == "FIRST_OF_MANUAL_REVIEW_NOT_AUTOMATIC_PAUSE":
                spend = review.get("after_incremental_spend", {})
                require(spend.get("currency") == "CNY" and isinstance(spend.get("amount"), (float, int))
                        and spend.get("amount") > 0 and spend.get("hard_cap") is False,
                        f"Invalid spend review metric: {exp_id}")
            elif mode == "SCHEDULED_SCRIPT_SUNSET_MANUAL_POST_CUTOFF_REVIEW":
                require(exp_id == "EXP-G2-PROMO-RSA-20261112", "Unexpected scheduled-sunset experiment")
                require(review.get("script_id") == "12708189" and review.get("script_cutoff_utc") == "2026-11-30T23:00:00Z",
                        "Incorrect G2 promo script/cutoff")
                require(sorted(review.get("ad_ids", [])) == ["831439588688", "831439627169"],
                        "Unexpected G2 promo ad whitelist")
                require(review.get("actual_sunset_verified") is False and review.get("not_an_exact_second_scheduler") is True,
                        "G2 actual sunset has not been observed")
            else:
                raise ControlError(f"Invalid review policy: {exp_id}")
    for mod in mods:
        for expid in mod.get("active_experiments", []):
            require(expid in exp_ids, f"Unknown active experiment {expid} in module {mod['id']}")

    jobs = tasks.get("tasks")
    require(isinstance(jobs, list), "Tasks is not a list")
    job_ids = [job.get("id") for job in jobs]
    require(None not in job_ids and len(job_ids) == len(set(job_ids)), "Duplicate/missing task IDs")
    for job in jobs:
        for field in ("experiment_id", "dependency"):
            if job.get(field):
                require(job[field] in exp_ids, f"Unknown {field}={job[field]} in {job['id']}")
        require(job.get("permission") in {"READ_ONLY", "DRAFT_ONLY", "WRITE_APPROVED", "SPEND_APPROVED"},
                f"Unrecognized permission in task {job['id']}")
    return portfolio, experiments, tasks


def show_status(portfolio, experiments, tasks):
    print(f"MaxSensual growth control | snapshot {portfolio['snapshot_as_of_date']} | HISTORICAL (not live API)")
    for exp in experiments["experiments"]:
        print(f"EXPERIMENT  {exp['id']}: {exp['status']}")
        if exp.get("status") == "ACTIVE":
            review = exp.get("review", {})
            if review.get("mode") == "FIRST_OF_MANUAL_REVIEW_NOT_AUTOMATIC_PAUSE":
                print(f"  manual review: +{review['after_incremental_spend']['amount']} {review['after_incremental_spend']['currency']}"
                      f" or {review['after_elapsed_days']} days (whichever first; NOT a hard cap)")
            else:
                print(f"  bounded sunset: script {review.get('script_id')} cutoff {review.get('script_cutoff_utc')};"
                      " actual post-cutoff pause still requires readback")
    for mod in portfolio["modules"]:
        print(f"MODULE      {mod['id']}: {mod['status_at_snapshot']}")
    print(f"TASKS       {len(tasks['tasks'])} tracked")
    print("CAUTION     No remote job, Shopify write, automatic gate or live synchronization is installed")


def check_change(experiments, resource):
    flagged = []
    for exp in experiments["experiments"]:
        if exp["status"] != "ACTIVE":
            continue
        guard = exp.get("change_guard", {})
        if any(fnmatch.fnmatchcase(resource, pattern) for pattern in guard.get("resource_patterns", [])):
            flagged.append(exp["id"])
    if flagged:
        print(f"APPROVAL_REQUIRED: {resource}\nProtected by active experiment(s): {', '.join(flagged)}")
        print("This is a human decision gate, NOT a remote lock. No changes were made.")
        return 2
    print(f"NO_KNOWN_CONFLICT: {resource}")
    print("This is not authorization; check live source and standard write approval before doing anything.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Validate JSON and cross-references; no external calls")
    sub.add_parser("status", help="Print the historical project control snapshot")
    check = sub.add_parser("check-change", help="Advisory manual-approval gate for a resource")
    check.add_argument("--resource", required=True, help="Example: shopify:collection:para-ella")
    args = parser.parse_args()
    try:
        p, e, t = load_and_validate()
        if args.command == "validate":
            print(f"PASS: {len(p['modules'])} modules, {len(e['experiments'])} experiments, {len(t['tasks'])} tasks")
            return 0
        if args.command == "status":
            show_status(p, e, t)
            return 0
        return check_change(e, args.resource)
    except ControlError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
