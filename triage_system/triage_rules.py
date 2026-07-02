# triage_rules.py
# All medical decision logic lives here

IMMEDIATE_SYMPTOMS = [
    'chest pain', 'crushing chest pain', 'cardiac arrest', 'no pulse',
    'unconscious', 'unresponsive', 'stroke', 'facial drooping',
    'slurred speech', 'anaphylaxis', 'severe allergic reaction',
    'uncontrolled bleeding', 'major bleeding', 'respiratory arrest',
    'not breathing', 'cyanosis', 'blue lips', 'septic shock', 'sepsis',
    'meningitis', 'non-blanching rash', 'seizure', 'severe burns',
]

URGENT_SYMPTOMS = [
    'moderate chest pain', 'chest tightness', 'shortness of breath',
    'difficulty breathing', 'confusion', 'disorientation',
    'severe abdominal pain', 'head injury', 'concussion',
    'fracture', 'suspected fracture', 'sudden severe headache',
    'thunderclap headache', 'stiff neck', 'diabetic emergency',
    'hypoglycemia', 'hyperglycemia', 'allergic reaction', 'lip swelling',
    'heavy bleeding', 'rectal bleeding', 'overdose', 'poisoning',
    'kidney stone', 'flank pain',
]

NORMAL_SYMPTOMS = [
    'moderate abdominal pain', 'stomach cramps', 'vomiting', 'diarrhoea',
    'urinary tract infection', 'painful urination', 'moderate back pain',
    'sprain', 'twisted ankle', 'moderate headache', 'ear pain',
    'ear infection', 'rash', 'dental abscess', 'toothache',
    'eye infection', 'conjunctivitis', 'musculoskeletal chest pain',
]

NON_URGENT_SYMPTOMS = [
    'common cold', 'runny nose', 'sore throat', 'mild headache',
    'minor cut', 'abrasion', 'muscle ache', 'insect bite',
    'mild nausea', 'constipation', 'mild rash', 'anxiety',
    'minor eye irritation', 'dry eyes', 'follow-up', 'wound check',
]


def assign_triage(patient):
    reasons = []
    score = 0

    # --- Check symptoms ---
    for symptom in patient.symptoms:
        if any(s in symptom for s in IMMEDIATE_SYMPTOMS):
            reasons.append(f"Critical symptom: {symptom}")
            score += 100

    for symptom in patient.symptoms:
        if any(s in symptom for s in URGENT_SYMPTOMS):
            if not any(s in symptom for s in IMMEDIATE_SYMPTOMS):
                reasons.append(f"Urgent symptom: {symptom}")
                score += 30

    for symptom in patient.symptoms:
        if any(s in symptom for s in NORMAL_SYMPTOMS):
            if not any(s in symptom for s in IMMEDIATE_SYMPTOMS + URGENT_SYMPTOMS):
                reasons.append(f"Moderate symptom: {symptom}")
                score += 12

    # --- Shortness of breath ---
    if patient.shortness_of_breath:
        reasons.append("Shortness of breath present")
        score += 40

    # --- Pulse ---
    if patient.pulse < 40 or patient.pulse > 150:
        reasons.append(f"Critical pulse: {patient.pulse} bpm")
        score += 60
    elif patient.pulse > 130:
        reasons.append(f"Dangerously high pulse: {patient.pulse} bpm")
        score += 40
    elif patient.pulse > 100:
        reasons.append(f"Elevated pulse: {patient.pulse} bpm")
        score += 20

    # --- Temperature ---
    if patient.fever > 41.0 or patient.fever < 35.0:
        reasons.append(f"Dangerous temperature: {patient.fever}°C")
        score += 60
    elif patient.fever >= 39.5:
        reasons.append(f"Very high fever: {patient.fever}°C")
        score += 35
    elif patient.fever >= 38.5:
        reasons.append(f"High fever: {patient.fever}°C")
        score += 20
    elif patient.fever >= 38.0:
        reasons.append(f"Mild fever: {patient.fever}°C")
        score += 10

    # --- Pain level ---
    if patient.pain_level >= 9:
        reasons.append(f"Extreme pain: {patient.pain_level}/10")
        score += 40
    elif patient.pain_level >= 7:
        reasons.append(f"Severe pain: {patient.pain_level}/10")
        score += 25
    elif patient.pain_level >= 5:
        reasons.append(f"Moderate pain: {patient.pain_level}/10")
        score += 12

    # --- Age ---
    if patient.age <= 2:
        reasons.append(f"Infant patient: {patient.age} years")
        score += 20
    elif patient.age >= 75:
        reasons.append(f"Elderly patient: {patient.age} years")
        score += 15
    elif patient.age >= 65:
        reasons.append(f"Older adult: {patient.age} years")
        score += 8

    # --- Final category ---
    if score >= 80:
        category = "IMMEDIATE"
    elif score >= 40:
        category = "URGENT"
    elif score >= 15:
        category = "NORMAL"
    else:
        category = "NON-URGENT"

    patient.triage_category = category
    patient.triage_reason = reasons if reasons else ["No acute indicators found"]
    return patient