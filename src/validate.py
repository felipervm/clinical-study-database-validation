"""Fictional clinical database edit-check demonstration. Standard library only."""
from __future__ import annotations
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "spec" / "rules.json").read_text())
BY_ID = {r["id"]: r for r in RULES}

def parse(value):
    try:
        return dt.date.fromisoformat(value) if isinstance(value, str) and len(value) == 10 and dt.date.fromisoformat(value).isoformat() == value else None
    except ValueError:
        return None

def validate(study):
    findings = []
    seen_subjects = set()
    def flag(subject, rule, detail, visit="—"):
        findings.append({"subject": subject, "visit": visit, "rule": rule, "detail": detail, "severity": BY_ID[rule]["severity"]})
    for subject in study["subjects"]:
        sid = subject["id"]
        consent = parse(subject.get("consent"))
        if sid in seen_subjects:
            flag(sid, "EC-07", "Repeated subject identifier")
        seen_subjects.add(sid)
        if consent is None:
            flag(sid, "EC-06", "Consent date is invalid")
        age = subject.get("age")
        if type(age) is not int or not 18 <= age <= 75:
            flag(sid, "EC-08", "Age outside fictional 18–75 criterion")
        visited = set()
        baseline = next((v for v in subject["visits"] if v["name"] == "Baseline"), None)
        base = parse(baseline["date"]) if baseline else None
        if base is None:
            flag(sid, "EC-06", "Baseline date missing or invalid")
        for visit in subject["visits"]:
            name = visit["name"]
            date = parse(visit.get("date"))
            if name in visited:
                flag(sid, "EC-05", "Duplicate visit label", name)
            visited.add(name)
            if date is None:
                flag(sid, "EC-06", "Visit date invalid", name)
            if date is not None and consent is not None and date < consent:
                flag(sid, "EC-01", "Visit occurred before consent", name)
            if date is not None and base is not None and name in ("Day 14", "Day 28"):
                offset = (date - base).days
                target = 14 if name == "Day 14" else 28
                if abs(offset - target) > 3:
                    flag(sid, "EC-02", f"Day {offset} is outside {name} ±3 day window", name)
            if visit.get("sbp") is None or visit.get("pulse") is None:
                flag(sid, "EC-03", "Systolic BP or pulse missing", name)
            sbp, pulse = visit.get("sbp"), visit.get("pulse")
            if ((type(sbp) in (int, float) and (sbp < 60 or sbp > 250)) or
                (type(pulse) in (int, float) and (pulse < 35 or pulse > 220))):
                flag(sid, "EC-04", "Unusual vital sign; needs human review", name)
    return sorted(findings, key=lambda r: (r["subject"], r["rule"]))

if __name__ == "__main__":
    study = json.loads((ROOT / "data" / "fictional_study.json").read_text())
    findings = validate(study)
    print(json.dumps({"study": study["study"], "fictional": True, "query_count": len(findings), "queries": findings}, indent=2))
