# Fictional study brief — OBS-26-001 (not a real protocol)

**Objective:** demonstrate traceable database design and edit checks for an illustrative observational study; no clinical hypothesis or efficacy evaluation.

**Illustrative visit schedule:** baseline (DAY 0), follow-up (DAY 14 ± 3), final (DAY 28 ± 3); study day is calculated relative to baseline. A visit may occur only on/after consent.

**Inclusion assumption:** age 18–75 inclusive at baseline. This is a made-up study rule and **not clinical advice**.

**Captured sections:** subject/consent date; age and sex-at-birth option; visit name/date; systolic blood pressure (SBP, mmHg) and heart rate (bpm).

**Important:** unusual SBP/HR does not imply an error; it creates a reviewable query only. No automatic correction or participant exclusion.

**Data design workflow:** requirement → field specification → edit check → UAT scenario → query log → human resolution.

**Exclusions:** adverse event capture, randomization, drug safety, dose, external lab systems and EDC integrations. These would require a much broader validated design.
