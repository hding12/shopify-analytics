import unittest
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.validate_growth_day import validate

class GrowthDayAuditTests(unittest.TestCase):
    def test_all_references(self):
        self.assertIn('PASS:', validate())

    def test_pmax_has_only_targeted_goal(self):
        entries=[json.loads(s) for s in (ROOT/'records/runs/2026-11-11-operations-addendum.jsonl').read_text().splitlines() if s.strip()]
        pmax=next(x for x in entries if x['event_id']=='RUN-DAY-20261111-001')
        self.assertEqual(pmax['changed_resources'], ['google_ads:campaignConversionGoal:24244298528~ADD_TO_CART~WEBSITE'])
        self.assertEqual(pmax['verification']['purchase_website_biddable'], True)

    def test_all_orders_are_merchant_qa(self):
        insights=json.loads((ROOT/'records/insights/2026-11-11-addendum.json').read_text())
        orders=next(x for x in insights if x['id']=='INS-DAY-20261111-002')
        self.assertEqual(sum(orders['scope']['amounts_clp']),15295)
        self.assertIn('0 CLP',orders['claim'])

    def test_recommendation_is_read_only(self):
        ops=[json.loads(s) for s in (ROOT/'records/runs/2026-11-11-operations-addendum.jsonl').read_text().splitlines() if s.strip()]
        for x in ops:
            if x['scope']=='hding12/maxsensual-recs' and 'dry run' in x['action'].lower():
                self.assertFalse(x['verification'].get('apply'))
        guards=json.loads((ROOT/'state/guards-2026-11-11-addendum.json').read_text())
        self.assertTrue(any(x['type']=='EXPLICIT_USER_NO_CHANGE' for x in guards['constraints']))

    def test_pixel_hypothesis_marked_rejected(self):
        insights=json.loads((ROOT/'records/insights/2026-11-11-addendum.json').read_text())
        claim=next(x for x in insights if x['id']=='INS-DAY-20261111-007')
        self.assertEqual(claim['status'],'REJECTED')
        self.assertIn('App Pixel',claim['claim'])

if __name__=='__main__': unittest.main()
