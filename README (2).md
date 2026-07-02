# Patient Triage System

## What this project does

This project is a small command-line programme written in Python that
simulates a basic hospital triage system. You enter a patient's vitals -
age, temperature, pulse, pain level, and whether they're short of breath -
and the programme decides how urgently they need to be seen, sorting them
into one of four categories: immediate, urgent, non-urgent, or normal.

It was built for the assignment "Develop a Python programme that
prioritises patients based on simple inputs."

## Getting started

You just need Python 3.8 or newer - nothing else to install.

```
git clone <your-repository-url>
cd <repository-folder>
python3 triage_system.py
```

## Walking through an example

When you run the programme, it asks for one patient's details:

```
--- TRIAGE SYSTEM: PATIENT INTAKE ---
Patient Name: Jane Doe
Patient Age (years): 45
Temperature (C): 37.0
Heart Rate (BPM): 80
Pain Scale (0-10): 1
Shortness of breath? (yes/no): no
```

Then it prints out the result:

```
========================================
 PATIENT REPORT: JANE DOE
 TRIAGE LEVEL  : NON-URGENT
========================================
```

If you type something invalid - a negative age, a temperature outside a
sane human range, an unrecognized yes/no answer - it tells you what went
wrong and asks again rather than crashing. Once a patient is done, you can
choose to enter another one or end the session.

## How the code is structured

The code is split into three parts so that each one only has to worry
about one thing:

- Patient is just a container for one patient's data. Its only bit of
  logic is normalizing the shortness-of-breath answer (which might come
  in as True/False, a string like "yes", or nothing at all) into a
  consistent "y"/"n" internally.
- TriageSystem holds the actual decision-making. Its evaluate_patient
  method takes a Patient and returns a category, and it doesn't know or
  care where that patient came from.
- run_triage_terminal() is everything to do with talking to the user:
  asking questions, validating answers, and printing the report.

Keeping the triage logic separate from the terminal interface is what
makes the logic testable. The test suite calls evaluate_patient() directly
with made-up patients, instead of having to fake keyboard input for every
single rule.

## The triage rules

The programme checks a patient against these rules in order, from most to
least urgent, and stops at the first one that fits:

1. Immediate - the patient is short of breath, or their pulse is above
   130 or below 40 BPM.
2. Urgent - high fever (39.0 C or above), critical hypothermia (35.0 C
   or below), or severe pain (8 out of 10 or above).
3. Non-urgent - mild pain (2 out of 10 or below), a stable temperature
   (between 36.0 C and 37.4 C), and the patient is older than 12.
4. Normal - anything that doesn't fit the above; the default, baseline
   case.

## Input limits

| Field | Accepted range |
|---|---|
| Age | 0 or above |
| Temperature | 32.0 C to 43.0 C |
| Heart rate | 0 to 250 BPM |
| Pain | 0 to 10 |
| Shortness of breath | yes / no |

## Testing

test_triage_system.py contains 49 unit tests covering the triage rules
(including boundary cases like exactly 130 BPM or exactly age 12), the
Patient data normalization, and the terminal's input validation. Run them
with:

```
python3 -m unittest test_triage_system -v
```

## What's in this repo

```
.
|-- triage_system.py        (Patient, TriageSystem, and the terminal loop)
|-- test_triage_system.py   (Unit tests)
`-- README.md
```

## Known limitations

- Nothing is saved between runs - it's a single-session console tool.
- The medical thresholds are simplified for the assignment and aren't
  based on a real clinical protocol (like ESI or the Manchester Triage
  System).
