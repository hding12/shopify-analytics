#!/usr/bin/env python3
"""Read-only schema and provenance checks for the 2026-11-11 growth audit addendum."""
from __future__ import annotations
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load(relative):
    path = ROOT / relative
    if not path.is_file():
        raise ValueError(f'Missing {relative}')
    def uniq(pairs):
        d = {}
        for key, val in pairs:
            if key in d: raise ValueError(f'Duplicate JSON key {key} in {relative}')
            d[key] = val
        return d
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=uniq)

def validate():
    ids = load('records/insights/2026-11-11-addendum.json')
    ds = load('records/decisions/2026-11-11-addendum.json')
    guards = load('state/guards-2026-11-11-addendum.json')
    ops = []
    path = ROOT / 'records/runs/2026-11-11-operations-addendum.jsonl'
    for lineno, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if line.strip():
            value = json.loads(line)
            if value.get('business_date') != '2026-11-11':
                raise ValueError(f'Unexpected business date in operations line {lineno}')
            ops.append(value)
    for name, rows in [('insights', ids), ('decisions', ds), ('operations', ops)]:
        if not isinstance(rows, list) or not rows:
            raise ValueError(name+' is empty/not list')
        key = 'event_id' if name == 'operations' else 'id'
        values = [x.get(key) for x in rows]
        if None in values or len(values) != len(set(values)):
            raise ValueError(name+' has duplicate or missing IDs')
    if guards.get('classification') != 'PUBLIC_HISTORICAL_SNAPSHOT_NOT_LIVE_PERMISSION':
        raise ValueError('Guard snapshot must not be represented as current authorization')
    gid = [x['id'] for x in guards.get('constraints', [])]
    if not gid or len(gid) != len(set(gid)):
        raise ValueError('Missing/duplicate guard IDs')
    opsids={x['event_id'] for x in ops}
    for d in ds:
        if d.get('status') not in {'ACTIVE','SUPERSEDED','REJECTED'}:
            raise ValueError('Invalid decision status: '+d['id'])
        if d.get('implementation_status') not in {'PROPOSED','APPROVED','EXECUTED','READBACK_VERIFIED','BLOCKED','ROLLED_BACK'}:
            raise ValueError('Invalid decision implementation status: '+d['id'])
        for ref in d.get('evidence', []):
            if ref.startswith('RUN-DAY-') and ref not in opsids:
                raise ValueError('Missing action ref '+ref)
    claim_states={'HYPOTHESIS','OBSERVED','VERIFIED','INCONCLUSIVE','REJECTED','SUPERSEDED'}
    execution_states={'PROPOSED','APPROVED','EXECUTED','READBACK_VERIFIED','BLOCKED','ROLLED_BACK'}
    for entry in ids:
        if entry.get('status') not in claim_states:
            raise ValueError('Invalid insight claim status '+entry['id'])
    for entry in ops:
        if entry.get('claim_status') not in claim_states:
            raise ValueError('Invalid operation claim status '+entry['event_id'])
        if entry.get('execution_status') is not None and entry['execution_status'] not in execution_states:
            raise ValueError('Invalid operation execution status '+entry['event_id'])
    rejects=[x for x in ids if x['status']=='REJECTED']
    if not any('pixel' in x.get('topic','') for x in rejects):
        raise ValueError('T08 disproved hypothesis must be preserved as REJECTED')
    if any(x.get('action','').startswith('Recommendation') and
           x['execution_status'].endswith('PUBLICATION_VERIFIED') for x in ops):
        raise ValueError('No recommendation publication is verified')
    market=load('control/experiments.json')
    ids_market = {x['id'] for x in market['experiments']}
    if 'EXP-PMAX-PURCHASE-ONLY-20261111' not in ids_market:
        raise ValueError('PMax experiment record missing; archive provenance broken')
    for name in ('docs/incidents/T08-2026-11-11-production-rollback.md',
                 'records/daily/2026-11-11-full-review.md',
                 'docs/methods-2026-11-11-addendum.md'):
        if not (ROOT/name).is_file(): raise ValueError('Missing '+name)
    return f'PASS: {len(ids)} insights, {len(ds)} decisions, {len(ops)} run entries, {len(gid)} guard records, PMax experiment cross-reference present'

if __name__=='__main__':
    try: print(validate())
    except (ValueError, KeyError, OSError) as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        raise SystemExit(1)
