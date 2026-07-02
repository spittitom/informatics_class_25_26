# main.py
# Runs the triage system

from patient import Patient
from triage_rules import assign_triage
from test_data import sample_patients

ICONS = {
    "IMMEDIATE":  "🔴",
    "URGENT":     "🟠",
    "NORMAL":     "🟡",
    "NON-URGENT": "🟢"
}

def display_result(patient):
    icon = ICONS[patient.triage_category]
    print("\n" + "=" * 50)
    print(f"  PATIENT : {patient.name}")
    print(f"  TRIAGE  : {icon}  {patient.triage_category}")
    print(f"  REASONS :")
    for r in patient.triage_reason:
        print(f"    - {r}")
    print("=" * 50)

def manual_input():
    print("\n--- Enter Patient Details ---")
    name         = input("Patient name: ")
    age          = int(input("Age: "))
    symptoms_raw = input("Symptoms (comma-separated, e.g. chest pain, dizziness): ")
    symptoms     = [s.strip() for s in symptoms_raw.split(",")]
    pain_level   = int(input("Pain level (0-10): "))
    fever        = float(input("Temperature in C (e.g. 37.5): "))
    pulse        = int(input("Pulse in bpm (e.g. 88): "))
    sob          = input("Shortness of breath? (yes / no): ").strip().lower()
    shortness    = sob in ["yes", "ja", "y"]

    p = Patient(name, age, symptoms, pain_level, fever, pulse, shortness)
    assign_triage(p)
    display_result(p)

def run_test_data():
    print("\n--- Running 4 Sample Patients ---")
    for p in sample_patients:
        assign_triage(p)
        display_result(p)

def main():
    print("\n==========================================")
    print("     PATIENT TRIAGE SYSTEM  v1.0")
    print("     Educational Use Only")
    print("==========================================")
    print("\n  1 - Enter a patient manually")
    print("  2 - Run sample test patients")
    choice = input("\nYour choice (1 or 2): ").strip()

    if choice == "1":
        manual_input()
    elif choice == "2":
        run_test_data()
    else:
        print("Invalid choice. Please run again and enter 1 or 2.")

if __name__ == "__main__":
    main()