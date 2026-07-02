# 🏥 Patient Triage System

> ⚠️ Educational project only — not a real medical decision tool.

A rule-based patient triage simulation system developed as part of a Health Informatics course at **Technische Hochschule Deggendorf (THD) / European Campus Rottal-Inn**. The system collects patient data and assigns a triage category based on clinical rules inspired by the **Manchester Triage System (MTS)** and **NEWS2 scoring**.

## Features
- Symptom checklist with 4 categories (Critical / Urgent / Moderate / Minor)
- Weighted scoring engine based on vitals and symptoms
- Four triage categories: 🔴 Immediate · 🟠 Urgent · 🟡 Normal · 🟢 Non-Urgent
- Session patient log table
- CSV export (opens in Excel)
- Python CLI + standalone web interface

## Files
| File | Purpose |
|---|---|
| `patient.py` | Patient data model |
| `triage_rules.py` | Scoring engine |
| `test_data.py` | Sample patients |
| `main.py` | CLI interface |
| `index.html` | Web frontend |

## How to Run
**Web:** Double-click `index.html` in any browser — no installation needed.

**Python CLI:**
```bash
python main.py
```

## Disclaimer
This system is an educational simulation only. Not for real clinical use.

## Author
Mariam — B.Sc. Health Informatics, THD Pfarrkirchen 🇩🇪
