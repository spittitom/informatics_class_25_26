# test_data.py
# Sample patients to test the system automatically

from patient import Patient

sample_patients = [
    Patient(
        name="Ahmed, 67",
        age=67,
        symptoms=["chest pain", "dizziness"],
        pain_level=9,
        fever=37.2,
        pulse=140,
        shortness_of_breath=True
    ),
    Patient(
        name="Klaus, 82",
        age=82,
        symptoms=["confusion", "weakness"],
        pain_level=3,
        fever=39.1,
        pulse=105,
        shortness_of_breath=False
    ),
    Patient(
        name="Sara, 34",
        age=34,
        symptoms=["headache", "nausea"],
        pain_level=4,
        fever=38.0,
        pulse=88,
        shortness_of_breath=False
    ),
    Patient(
        name="Lena, 22",
        age=22,
        symptoms=["sore throat", "mild cough"],
        pain_level=2,
        fever=37.5,
        pulse=72,
        shortness_of_breath=False
    ),
]