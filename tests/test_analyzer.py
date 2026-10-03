import unittest

from fitness_analyzer.csv_reader import load_participants, load_sessions
from fitness_analyzer.exceptions import (
    InvalidIdentifierError,
    InvalidRecordError,
)
from fitness_analyzer.validation import (
    validate_participant_id,
    validate_session_id,
    validate_heart_rate,
    validate_signal_quality,
)


class TestFitnessAnalyzer(unittest.TestCase):

    def test_valid_identifiers(self):
        self.assertTrue(validate_participant_id("P001"))
        self.assertTrue(validate_session_id("FIT-2026-001"))

    def test_invalid_identifiers(self):
        with self.assertRaises(InvalidIdentifierError):
            validate_participant_id("001")

        with self.assertRaises(InvalidIdentifierError):
            validate_session_id("FIT-26-001")

    def test_boundary_values(self):
        self.assertTrue(validate_heart_rate(35))
        self.assertTrue(validate_heart_rate(205))
        self.assertTrue(validate_signal_quality(0.5))
        self.assertTrue(validate_signal_quality(1.0))

        with self.assertRaises(InvalidRecordError):
            validate_heart_rate(34)

        with self.assertRaises(InvalidRecordError):
            validate_heart_rate(206)

    def test_invalid_file_records_are_rejected(self):
        participants = load_participants("data/participants.csv")

        sessions, rejected = load_sessions(
            "data/fitness_sessions_invalid.csv",
            participants,
        )

        self.assertGreater(len(rejected), 0)
        self.assertGreater(len(sessions), 0)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_sessions(
                "data/does_not_exist.csv",
                {},
            )


if __name__ == "__main__":
    unittest.main()