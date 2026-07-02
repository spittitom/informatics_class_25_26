class Patient:
    """
    Data class representing a single patient.
    Groups all physiological inputs and text attributes into one structural object.
    """
    def __init__(self, name, age, temperature, pulse, pain, shortness_of_breath):
        self.name = name
        self.age = age
        self.temperature = temperature 
        self.pulse = pulse
        self.pain = pain
        
        # Safe serialization type-guard
        if isinstance(shortness_of_breath, bool):
            self.shortness_of_breath = "y" if shortness_of_breath else "n"
        elif shortness_of_breath is not None:
            self.shortness_of_breath = str(shortness_of_breath).lower().strip()[:1]
        else:
            self.shortness_of_breath = "n"


class TriageSystem:
    """
    Logic engine that holds the core evaluation algorithms.
    Contains no user interface code, separating data processing from console input/output.
    """
    def evaluate_patient(self, patient):
        # Category 1: Immediate Priority (Life-threatening symptoms or extreme vitals)
        if patient.shortness_of_breath == "y" or patient.pulse > 130 or patient.pulse < 40:
            return "immediate"
        
        # Category 2: Urgent Priority (High fever, severe pain, or critical hypothermia)
        elif patient.temperature >= 39.0 or patient.temperature <= 35.0 or patient.pain >= 8:
            return "urgent"
        
        # Category 3: Non-Urgent Priority (Mild symptoms, stable temperature window, adult/teen)
        elif patient.pain <= 2 and (36.0 <= patient.temperature < 37.5) and patient.age > 12:
            return "non-urgent"
        
        # Category 4: Normal Priority (Standard baseline triage case)
        else:
            return "normal"


def run_triage_terminal():
    """
    User Interface (UI) handler.
    Manages the live system terminal, safe input loop guards, and reporting screens.
    """
    triage_tool = TriageSystem()
    
    while True:
        print("\n--- TRIAGE SYSTEM: PATIENT INTAKE ---")

        patient_name = input("Patient Name: ").strip()
        if not patient_name:
            patient_name = "Anonymous"
        
        # 1. Age Input Protection Guard
        while True:
            try:
                patient_age = int(input("Patient Age (years): "))
                if patient_age < 0:
                    print("❌ ERROR: Age cannot be negative.")
                    continue
                break
            except ValueError:
                print("❌ ERROR: Invalid input. Please enter a whole number.")

        # 2. Temperature Input Protection Guard
        while True:
            try:
                body_temp = float(input("Temperature (°C): "))
                if body_temp < 32.0 or body_temp > 43.0:
                    print("❌ ERROR: Invalid range. Temperature must be between 32.0°C and 43.0°C.")
                    continue
                break
            except ValueError:
                print("❌ ERROR: Invalid input. Please enter a decimal number.")

        # 3. Heart Rate Input Protection Guard
        while True:
            try:
                heart_rate = int(input("Heart Rate (BPM): "))
                if heart_rate < 0 or heart_rate > 250:
                    print("❌ ERROR: Invalid range. Heart rate must be between 0 and 250 BPM.")
                    continue
                break
            except ValueError:
                print("❌ ERROR: Invalid input. Please enter a whole number.")

        # 4. Pain Scale Input Protection Guard
        while True:
            try:
                pain_scale = int(input("Pain Scale (0-10): "))  
                if pain_scale < 0 or pain_scale > 10:
                    print("❌ ERROR: Pain scale must be between 0 and 10.")
                    continue
                break
            except ValueError:
                print("❌ ERROR: Invalid input. Please enter a whole number.")

        # 5. Shortness of Breath Input Guard
        while True:
            has_sob = input("Shortness of breath? (yes/no): ").strip().lower()
            if has_sob in ['y', 'yes', 'n', 'no']:
                break
            print("❌ ERROR: Invalid input. Please type 'yes' or 'no'.")

        # Object Creation
        current_patient = Patient(
            name=patient_name,
            age=patient_age,
            temperature=body_temp,
            pulse=heart_rate,
            pain=pain_scale,
            shortness_of_breath=has_sob
        )

        # Logic Processing
        assigned_triage = triage_tool.evaluate_patient(current_patient)

        # Output Interface Screen Display
        print("\n========================================")
        print(f" PATIENT REPORT: {current_patient.name.upper()}")
        print(f" TRIAGE LEVEL  : {assigned_triage.upper()}")
        print("========================================")

        # Continuation Loop Guard
        while True:
            next_patient = input("\nReady for the next patient? (yes/no): ").strip().lower()[:1]
            if next_patient == 'y':
                break
            elif next_patient == 'n':
                print("\n[System Logged Out] Session ended.")
                return
            else:
                print("❌ ERROR: Invalid input. Please type 'yes' or 'no'.")


if __name__ == "__main__":
    run_triage_terminal()
