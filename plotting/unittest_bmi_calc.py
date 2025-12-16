import unittest

# --- Zu testende Funktion (aus dem Hauptcode kopiert) ---
def calculate_all_bmi(patient_data: list) -> list:
    """Calculates the BMI for all patients in the list. (Weight/Height^2)"""
    weight = [p[1] for p in patient_data]
    height = [p[2] for p in patient_data]
    
    # Error handling for invalid data
    if any(h <= 0 for h in height):
        raise ValueError("Height must be positive.")
        
    return [w / (h ** 2) for w, h in zip(weight, height)]
# --------------------------------------------------------

class TestBMIFunktion(unittest.TestCase):
    
    # Testfall 1: Überprüfung der Listen-Verarbeitung (NEU)
    def test_calculate_all_bmi_list(self):
        """
        Testet die 'calculate_all_bmi'-Funktion mit mehreren Datensätzen und
        überprüft, ob alle BMI-Werte korrekt berechnet werden.
        """
        # Datenformat: (Alter, Gewicht_kg, Größe_m)
        patient_data = [
            (25, 75, 1.80), # BMI ≈ 23.15
            (55, 95, 1.75), # BMI ≈ 31.02
            (30, 50, 1.65)  # BMI ≈ 18.37
        ]
        
        # Erwartete BMIs (gerundet auf 2 Nachkommastellen)
        expected_bmis = [23.15, 31.02, 18.37] 
        
        calculated_bmis = calculate_all_bmi(patient_data)
        
        self.assertEqual(len(calculated_bmis), len(expected_bmis))
        
        # Überprüfung jedes einzelnen Wertes auf nahezu Gleichheit
        for calculated, expected in zip(calculated_bmis, expected_bmis):
            self.assertAlmostEqual(calculated, expected, places=2)

    # Testfall 2: Überprüfung der Fehlerbehandlung bei ungültiger Größe (NEU)
    def test_calculate_all_bmi_invalid_height(self):
        """
        Testet die Fehlerbehandlung, wenn in der Liste ungültige Höhenwerte
        (Null oder negativ) vorhanden sind.
        """
        # Zweiter Patient hat ungültige Größe (0)
        invalid_data = [
            (25, 75, 1.80), 
            (55, 95, 0.0) 
        ]
        
        # Es wird erwartet, dass ein ValueError ausgelöst wird
        with self.assertRaises(ValueError):
            calculate_all_bmi(invalid_data)

    # (Die Einzeltests für die Single-BMI-Berechnung vom letzten Mal können 
    #  hier beibehalten werden, um die separate Logik zu testen.)
    
# Führen Sie die Tests aus
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)