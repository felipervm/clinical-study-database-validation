import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from validate import validate,parse

class TestEditChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study=json.loads((ROOT/"data"/"fictional_study.json").read_text())
        cls.findings=validate(cls.study)

    def test_dates_reject_impossible_days(self):
        self.assertIsNone(parse("2026-02-30"))
        self.assertIsNone(parse("bad-date"))

    def test_known_valid_subject_has_no_queries(self):
        self.assertFalse([q for q in self.findings if q["subject"]=="S-001"])

    def test_chronology(self):
        self.assertTrue(any(q["subject"]=="S-002" and q["rule"]=="EC-01" for q in self.findings))

    def test_visit_window(self):
        self.assertTrue(any(q["subject"]=="S-003" and q["rule"]=="EC-02" for q in self.findings))

    def test_missing_vitals(self):
        self.assertTrue(any(q["subject"]=="S-003" and q["rule"]=="EC-03" for q in self.findings))

    def test_duplicate_visit(self):
        self.assertTrue(any(q["subject"]=="S-003" and q["rule"]=="EC-05" for q in self.findings))

    def test_plausibility(self):
        self.assertTrue(any(q["subject"]=="S-004" and q["rule"]=="EC-04" for q in self.findings))

    def test_fictional_age_rule(self):
        self.assertTrue(any(q["subject"]=="S-004" and q["rule"]=="EC-08" for q in self.findings))

    def test_bad_consent_date(self):
        self.assertTrue(any(q["subject"]=="S-005" and q["rule"]=="EC-06" for q in self.findings))

    def test_missing_baseline(self):
        self.assertTrue(any(q["subject"]=="S-006" and q["rule"]=="EC-06" for q in self.findings))

    def test_duplicate_subject_register(self):
        dup=json.loads(json.dumps(self.study))
        dup["subjects"].append(dict(dup["subjects"][0]))
        self.assertTrue(any(q["rule"]=="EC-07" for q in validate(dup)))

    def test_traceability(self):
        rules=json.loads((ROOT/"spec"/"rules.json").read_text())
        ids={r["id"] for r in rules}
        self.assertEqual(len(ids),8)
        self.assertTrue(all(q["rule"] in ids for q in self.findings))

if __name__=="__main__":
    unittest.main()
