# 🏥 Patient Triage System

> ⚠️ **Educational project only — not a real medical decision tool.**

A rule-based patient triage simulation system developed as part of a Health Informatics course at **Technische Hochschule Deggendorf (THD) / European Campus Rottal-Inn**. The system collects patient data and assigns a triage category based on clinical rules inspired by the **Manchester Triage System (MTS)** and **NEWS2 scoring**.

---

## 📸 Preview

> Web interface — open `index.html` in any browser, no installation needed.

The form accepts patient details, lets staff select symptoms from a categorised checklist, and returns a colour-coded triage result with clinical reasoning and a downloadable CSV log.

---

## 📌 Features

- ✅ Symptom selection from a categorised checklist (Critical / Urgent / Moderate / Minor)
- ✅ Weighted scoring engine based on vitals and symptoms
- ✅ Assigns one of four triage categories with colour coding
- ✅ Displays detailed reasons for each decision
- ✅ Logs all triaged patients in a session table
- ✅ Exports results as a downloadable **CSV file** (opens in Excel)
- ✅ Python CLI version for terminal use
- ✅ No external libraries needed for the web version

---

## 🎯 Triage Categories

| Category | Colour | Max Wait | Description |
|---|---|---|---|
| **Immediate** | 🔴 Red | 0 min | Life-threatening — act now |
| **Urgent** | 🟠 Orange | 10 min | Serious — needs quick attention |
| **Normal** | 🟡 Yellow | 30 min | Significant but stable |
| **Non-Urgent** | 🟢 Green | 120 min | Minor complaint |

---

## 🗂️ Project Structure

```
triage_system/
├── index.html          # Web frontend — standalone, open in any browser
├── patient.py          # Patient data model (Python class)
├── triage_rules.py     # Medical scoring and decision logic
├── test_data.py        # Sample patients for testing
└── main.py             # Python CLI version
```

---

## 🚀 How to Run

### Option 1 — Web Interface (recommended)

No installation needed. Just:

1. Download or clone the repository
2. Double-click `index.html`
3. It opens directly in your browser

### Option 2 — Python CLI

```bash
python main.py
```

Then choose:
- `1` — Enter a patient manually
- `2` — Run the 4 built-in sample test patients

**Requirements:** Python 3.x — no external packages needed.

---

## 🧠 Medical Foundation

### Scoring Logic

The triage engine assigns points per input and categorises based on the total score:

| Score | Category |
|---|---|
| ≥ 80 | 🔴 Immediate |
| ≥ 40 | 🟠 Urgent |
| ≥ 15 | 🟡 Normal |
| < 15 | 🟢 Non-Urgent |

### Vital Sign Thresholds

| Input | Trigger | Points Added |
|---|---|---|
| Pulse | > 150 or < 40 bpm | +60 |
| Pulse | > 130 bpm | +40 |
| Pulse | > 100 bpm | +20 |
| Temperature | > 41°C or < 35°C | +60 |
| Temperature | ≥ 39.5°C | +35 |
| Temperature | ≥ 38.5°C | +20 |
| Pain level | ≥ 9 / 10 | +40 |
| Pain level | ≥ 7 / 10 | +25 |
| Shortness of breath | Present | +40 |
| Age | ≤ 2 or ≥ 75 years | +15–20 |

### Symptom Categories

| Level | Example Symptoms |
|---|---|
| 🔴 Critical (+100 pts each) | Chest pain, cardiac arrest, stroke, seizure, anaphylaxis, cyanosis, sepsis |
| 🟠 Urgent (+30 pts each) | Confusion, fracture, severe abdominal pain, overdose, stiff neck, heavy bleeding |
| 🟡 Moderate (+12 pts each) | Vomiting, UTI, ear infection, moderate headache, sprain, dental abscess |
| 🟢 Minor (+4 pts each) | Sore throat, mild nausea, insect bite, anxiety, minor cut, constipation |

---

## 🧪 Sample Test Results

| Patient | Age | Key Symptoms | Fever | Pulse | Pain | SOB | Result |
|---|---|---|---|---|---|---|---|
| Ahmed | 67 | Chest pain, dizziness | 37.2°C | 140 | 9/10 | Yes | 🔴 Immediate |
| Klaus | 82 | Confusion, weakness | 39.1°C | 105 | 3/10 | No | 🟠 Urgent |
| Sara | 34 | Headache, nausea | 38.0°C | 88 | 4/10 | No | 🟡 Normal |
| Lena | 22 | Sore throat, mild cough | 37.5°C | 72 | 2/10 | No | 🟢 Non-Urgent |

---

## 🛠️ Technologies Used

| Layer | Technology |
|---|---|
| Core logic | Python 3 (OOP, rule-based engine) |
| Web frontend | HTML5 / CSS3 / Vanilla JavaScript |
| Data export | Browser Blob API → CSV |
| Medical basis | Manchester Triage System, NEWS2 |

---

## 📋 CSV Export Format

Each row in the exported file contains:

```
#, Name, Age, Symptoms, Pain Level, Temperature (C), Pulse (bpm), Shortness of Breath, Triage Category, Timestamp
```

---

## 📚 References

- Manchester Triage Group — *Emergency Triage*, 3rd Edition
- Royal College of Physicians — *NEWS2 (National Early Warning Score)* Documentation
- World Health Organization — *Emergency Triage Assessment and Treatment (ETAT)*

---

## ⚠️ Disclaimer

This system is a **university educational project and simulation only**. It does not constitute medical advice and must never be used for real clinical decisions. All triage decisions must be made by qualified medical professionals.

---

## 👩‍💻 Author

**Mariam**  
B.Sc. Health Informatics — Technische Hochschule Deggendorf  
European Campus Rottal-Inn, Pfarrkirchen, Bavaria 🇩🇪

---

## 🏷️ Topics

`python` `health-informatics` `triage` `medical-simulation` `rule-based-system` `html` `javascript` `csv` `manchester-triage-system` `news2` `educational`
