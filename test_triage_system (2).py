"""
Unit tests for triage_system.py

Covers:
  - Patient: shortness_of_breath normalization for every input type
  - TriageSystem.evaluate_patient: all four categories, boundary values,
    and category-precedence ordering
  - run_triage_terminal: happy path + every input-validation guard
    (age, temperature, heart rate, pain scale, SOB, continuation loop),
    driven via mocked input()/print() so no real console I/O occurs.
"""
import unittest
from unittest.mock import patch, call

from triage_system import Patient, TriageSystem, run_triage_terminal


# ---------------------------------------------------------------------------
# Patient
# ---------------------------------------------------------------------------
class TestPatientShortnessOfBreathNormalization(unittest.TestCase):

    def _sob(self, value):
        return Patient("X", 30, 37.0, 80, 0, value).shortness_of_breath

    def test_bool_true_becomes_y(self):
        self.assertEqual(self._sob(True), "y")

    def test_bool_false_becomes_n(self):
        self.assertEqual(self._sob(False), "n")

    def test_none_becomes_n(self):
        self.assertEqual(self._sob(None), "n")

    def test_string_yes_becomes_y(self):
        self.assertEqual(self._sob("yes"), "y")

    def test_string_y_becomes_y(self):
        self.assertEqual(self._sob("y"), "y")

    def test_string_no_becomes_n(self):
        self.assertEqual(self._sob("no"), "n")

    def test_string_uppercase_is_lowercased(self):
        self.assertEqual(self._sob("YES"), "y")

    def test_string_with_whitespace_is_stripped(self):
        self.assertEqual(self._sob("  yes  "), "y")

    def test_empty_string_becomes_empty(self):
        # "".strip()[:1] -> "" which matches neither "y" nor triggers None branch
        self.assertEqual(self._sob(""), "")

    def test_other_object_is_stringified(self):
        self.assertEqual(self._sob(123), "1")

    def test_basic_attribute_assignment(self):
        p = Patient("Alice", 40, 37.2, 75, 3, "no")
        self.assertEqual(p.name, "Alice")
        self.assertEqual(p.age, 40)
        self.assertEqual(p.temperature, 37.2)
        self.assertEqual(p.pulse, 75)
        self.assertEqual(p.pain, 3)
        self.assertEqual(p.shortness_of_breath, "n")


# ---------------------------------------------------------------------------
# TriageSystem.evaluate_patient
# ---------------------------------------------------------------------------
class TestTriageImmediate(unittest.TestCase):
    def setUp(self):
        self.triage = TriageSystem()

    def test_shortness_of_breath_triggers_immediate(self):
        p = Patient("A", 30, 37.0, 80, 0, "y")
        self.assertEqual(self.triage.evaluate_patient(p), "immediate")

    def test_pulse_above_130_triggers_immediate(self):
        p = Patient("A", 30, 37.0, 131, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "immediate")

    def test_pulse_at_130_is_not_immediate(self):
        # boundary: > 130 required, 130 itself should not trigger this branch
        p = Patient("A", 30, 37.0, 130, 0, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "immediate")

    def test_pulse_below_40_triggers_immediate(self):
        p = Patient("A", 30, 37.0, 39, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "immediate")

    def test_pulse_at_40_is_not_immediate(self):
        p = Patient("A", 30, 37.0, 40, 0, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "immediate")

    def test_immediate_takes_precedence_over_urgent(self):
        # High fever AND SOB -> immediate wins
        p = Patient("A", 30, 40.0, 80, 9, "y")
        self.assertEqual(self.triage.evaluate_patient(p), "immediate")


class TestTriageUrgent(unittest.TestCase):
    def setUp(self):
        self.triage = TriageSystem()

    def test_high_fever_at_39_triggers_urgent(self):
        p = Patient("A", 30, 39.0, 80, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "urgent")

    def test_fever_just_below_39_is_not_urgent_on_temp_alone(self):
        p = Patient("A", 30, 38.9, 80, 0, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "urgent")

    def test_hypothermia_at_35_triggers_urgent(self):
        p = Patient("A", 30, 35.0, 80, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "urgent")

    def test_temp_just_above_35_is_not_urgent_on_temp_alone(self):
        p = Patient("A", 30, 35.1, 80, 0, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "urgent")

    def test_severe_pain_at_8_triggers_urgent(self):
        p = Patient("A", 30, 37.0, 80, 8, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "urgent")

    def test_pain_at_7_does_not_trigger_urgent_on_pain_alone(self):
        p = Patient("A", 30, 37.0, 80, 7, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "urgent")

    def test_urgent_takes_precedence_over_non_urgent(self):
        # Low pain + normal temp window would normally be non-urgent,
        # but pain>=8 forces urgent. Use fever instead since pain<=2 is
        # required for non-urgent; test with fever + otherwise mild profile.
        p = Patient("A", 30, 39.5, 80, 1, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "urgent")


class TestTriageNonUrgent(unittest.TestCase):
    def setUp(self):
        self.triage = TriageSystem()

    def test_mild_adult_case_is_non_urgent(self):
        p = Patient("A", 30, 36.5, 80, 1, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "non-urgent")

    def test_pain_at_2_is_non_urgent(self):
        p = Patient("A", 30, 36.5, 80, 2, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "non-urgent")

    def test_pain_at_3_is_not_non_urgent(self):
        p = Patient("A", 30, 36.5, 80, 3, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "non-urgent")

    def test_temp_lower_bound_36_included(self):
        p = Patient("A", 30, 36.0, 80, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "non-urgent")

    def test_temp_just_below_36_excluded(self):
        p = Patient("A", 30, 35.9, 80, 0, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "non-urgent")

    def test_temp_upper_bound_37_5_excluded(self):
        p = Patient("A", 30, 37.5, 80, 0, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "non-urgent")

    def test_temp_just_below_37_5_included(self):
        p = Patient("A", 30, 37.4, 80, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "non-urgent")

    def test_age_13_included(self):
        p = Patient("A", 13, 36.5, 80, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "non-urgent")

    def test_age_12_excluded(self):
        p = Patient("A", 12, 36.5, 80, 0, "n")
        self.assertNotEqual(self.triage.evaluate_patient(p), "non-urgent")


class TestTriageNormal(unittest.TestCase):
    def setUp(self):
        self.triage = TriageSystem()

    def test_falls_through_to_normal_when_child_with_mild_symptoms(self):
        # Mild vitals but age <=12 disqualifies non-urgent
        p = Patient("Child", 10, 36.5, 80, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "normal")

    def test_falls_through_to_normal_when_moderate_pain_and_stable_temp(self):
        # pain=5 disqualifies non-urgent, but doesn't reach urgent threshold
        p = Patient("A", 30, 36.5, 80, 5, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "normal")

    def test_falls_through_to_normal_when_temp_out_of_non_urgent_window_only(self):
        p = Patient("A", 30, 38.0, 80, 0, "n")
        self.assertEqual(self.triage.evaluate_patient(p), "normal")


# ---------------------------------------------------------------------------
# run_triage_terminal (console UI loop)
# ---------------------------------------------------------------------------
class TestRunTriageTerminal(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.input")
    def test_happy_path_single_patient_then_quit(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Jane Doe",   # name
            "45",         # age
            "37.0",       # temperature
            "80",         # heart rate
            "1",          # pain
            "no",         # SOB
            "no",         # don't continue -> exit
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("JANE DOE", printed)
        self.assertIn("NON-URGENT", printed)
        self.assertIn("Session ended", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_blank_name_defaults_to_anonymous(self, mock_input, mock_print):
        mock_input.side_effect = [
            "",           # blank name -> Anonymous
            "30", "37.0", "80", "0", "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("ANONYMOUS", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_negative_age_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob",
            "-5", "40",   # age: reject negative, then accept
            "37.0", "80", "0", "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Age cannot be negative", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_non_numeric_age_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob",
            "not-a-number", "40",
            "37.0", "80", "0", "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Please enter a whole number", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_out_of_range_temperature_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40",
            "50.0", "37.0",   # too high, then valid
            "80", "0", "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Temperature must be between", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_non_numeric_temperature_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40",
            "hot", "37.0",
            "80", "0", "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Please enter a decimal number", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_out_of_range_heart_rate_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40", "37.0",
            "300", "80",   # too high, then valid
            "0", "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Heart rate must be between", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_non_numeric_heart_rate_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40", "37.0",
            "fast", "80",
            "0", "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Please enter a whole number", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_out_of_range_pain_scale_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40", "37.0", "80",
            "15", "3",    # too high, then valid
            "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Pain scale must be between", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_non_numeric_pain_scale_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40", "37.0", "80",
            "ouch", "3",
            "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Please enter a whole number", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_invalid_sob_answer_is_rejected_then_accepted(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40", "37.0", "80", "3",
            "maybe", "yes",   # invalid, then valid
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Please type 'yes' or 'no'", printed)
        self.assertIn("IMMEDIATE", printed)  # sob=yes -> immediate

    @patch("builtins.print")
    @patch("builtins.input")
    def test_invalid_continuation_answer_is_rejected_then_quits(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40", "37.0", "80", "3", "no",
            "maybe", "no",   # invalid continuation, then quit
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Please type 'yes' or 'no'", printed)
        self.assertIn("Session ended", printed)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_continue_yes_processes_second_patient(self, mock_input, mock_print):
        mock_input.side_effect = [
            "Bob", "40", "37.0", "80", "3", "no",
            "yes",                                 # continue to next patient
            "Alice", "70", "39.5", "90", "9", "no",
            "no",
        ]
        run_triage_terminal()
        printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("BOB", printed)
        self.assertIn("ALICE", printed)
        self.assertIn("URGENT", printed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
