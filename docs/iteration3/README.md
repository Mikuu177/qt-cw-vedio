# Iteration 3 Documentation (Final)

## Overview
This folder contains all documentation and artifacts from Iteration 3 (Final Refinement phase).

## Key Artifacts
- ITERATION3_FINAL_RECORD.md — Final iteration record (goals, changes, implementation, testing, deliverables)
- evaluation3_report.md — SUS questionnaire findings (if applicable)
- performance_testing.md — Performance optimization results (if applicable)
- ../.. /EXPORT_FIX_REPORT.md — Detailed export (FFmpeg) fix report
- ../.. /EXPORT_FIX_SUMMARY.md — Export fix summary (quick read)
- ../.. /EXPORT_QUICK_GUIDE.md — Export quick user guide
- /screenshots — Final UI screenshots (optional)

## Code & Tests
- Authentication (login/register/forgot): `src/utils/auth_manager.py`, `src/ui/auth_dialogs.py`, `src/main_v2.py`, `src/ui/main_window_v2.py`
- i18n resources: `src/resources/strings_en.json`, `src/resources/strings_zh.json`
- Export/Concatenate tests:
  - `test_concatenate.py`
  - `test_export_simple.py`

## How to Run
```bash
# From project root
python src/main_v2.py
```

## Links
- Final iteration record: `docs/iteration3/ITERATION3_FINAL_RECORD.md`
- Project status & guides are in project root:
  - `EXPORT_FIX_REPORT.md`
  - `EXPORT_FIX_SUMMARY.md`
  - `EXPORT_QUICK_GUIDE.md`

## Timeline
Week 3–4 (Final)

## Deliverables
- Prototype v3 (final)
- Internationalization complete (EN/zh)
- Authentication added (login/register/forgot)
- Export flow fixed and verified
- Iteration 3 record and supporting documents
