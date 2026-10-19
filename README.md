# Clinical Study Database Design & Validation
**Independent proof of work by Felipe Mattos** · Fictional study · Not affiliated with Everest Clinical Research

## The problem worth solving
A study database should translate a protocol into consistent data capture, predictable checks, and reviewable exceptions **before go-live**. A persuasive database-design sample should connect a stated requirement to an eCRF field, an edit check, and a UAT result—not merely show a dashboard.

## Scope (V1)
- Fictional, single-arm observational study `OBS-26-001`, not a genuine clinical protocol.
- **4 CRF sections**: informed consent, demographics, visits and vital signs.
- **8 traceable rules**: consent chronology, visit window, missing measurements, physiological plausibility, duplicate visits, date bounds, duplicate subject IDs, and age eligibility.
- Synthetic records containing intentional errors. The visible website demonstrates how queries are generated, never silently "corrects" a patient record.
- Python standard-library validator (`src/validate.py`), machine-readable eCRF specification (`spec/fields.json`), edit check catalog (`spec/rules.json`), UAT cases (`tests/test_validation.py`).
- Read-only interactive review with synthetic examples, traceability matrix and clear limits.

## Why this task is relevant to the position
The published **Clinical Database Designer I** description at Everest Clinical Research mentions eCRF design, edit checks, test/UAT, database modifications, specifications, and QA. The sample demonstrates transferable workflow literacy. **It does not claim EDC-platform experience** or regulatory validation.

## How to run locally
```sh
python src/validate.py
python -m unittest discover -s tests -v
python -m http.server 8000
```
Then open `http://localhost:8000`. Python 3.10+ recommended; no packages required.

## Methodology and safety
- All participant identifiers, visit dates, and vital signs are fabricated.
- Ranges, visit windows and the protocol are researcher's **illustrative assumptions**; not Everest clinical SOPs, CDISC-certified metadata, medical advice, or validated protocol limits.
- Flagged values are **review queries**, not determinations of clinical correctness.
- No identifiable patient information, external API, live EDC, credentials or actual clinical-study data.
- This is not an authenticated, audit-trailed EDC platform and is **not suitable for regulated study use**. Production would require validated requirements, access controls, change control, audit trails, vendor qualification and formal UAT.

## Public design references
- [CDISC CDASH / CDASHIG 2.1](https://www.cdisc.org/standards/foundational/cdashig-v2-1) — clinical data acquisition conventions, not a certification of this demo.
- [FDA — Electronic Source Data in Clinical Investigations](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-source-data-clinical-investigations) — reliability, integrity and traceability of eSource/eCRF data.
- [FDA — Computerized Systems Used in Clinical Trials](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/fda-bioresearch-monitoring-information/guidance-industry-computerized-systems-used-clinical-trials) — audit trail and change-recording expectations.

## Intended outreach
Interested in opportunities in **clinical database design, data validation, data quality or junior clinical data operations**. This sample is a conversation starter to demonstrate a credible way to approach the work, not a substitute for the role's one-year EDC experience.
