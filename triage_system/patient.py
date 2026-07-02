# patient.py
# Stores all information about one patient

class Patient:
    def __init__(self, name, age, symptoms, pain_level, fever, pulse, shortness_of_breath):
        self.name = name
        self.age = age
        self.symptoms = [s.lower().strip() for s in symptoms]
        self.pain_level = pain_level        # 0–10
        self.fever = fever                  # °C
        self.pulse = pulse                  # beats per minute
        self.shortness_of_breath = shortness_of_breath  # True or False
        self.triage_category = None         # assigned later
        self.triage_reason = []             # reasons list