import csv

from fitness_analyzer.models import (Participant, ReferenceProfile, Observation, FitnessSession)
from fitness_analyzer.validation import (
    validate_participant_id,
    validate_session_id,
)
from fitness_analyzer.exceptions import InvalidIdentifierError

def load_participants(file_path):
    participants = {}
    with open(file_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                validate_participant_id(row["participant_id"])

                reference_profile = ReferenceProfile(
                    int(row["baseline_heart_rate"]),
                    float(row["baseline_skin_response"]),
                    float(row["baseline_temperature"])
                )
                participant = Participant(
                    row["participant_id"],
                    reference_profile,
                )
                participants[row["participant_id"]] = participant
            except (InvalidIdentifierError, ValueError) as error:
                print("Rejected participant row:", error)
    return participants


def load_sessions(file_path, participants):
    sessions = {}

    with open(file_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            validate_session_id(row["session_id"])
            validate_participant_id(row["participant_id"])

            if row["participant_id"] not in participants:
                raise InvalidIdentifierError(
                    f"Unknown participant ID: {row['participant_id']}"
                )

            observation = Observation(
                int(row["timestamp"]),
                int(row["heart_rate"]),
                float(row["skin_response"]),
                float(row["temperature"]),
                float(row["activity_level"]),
                float(row["signal_quality"]),
            )

            session_id = row["session_id"]

            if session_id not in sessions:
                participant = participants[row["participant_id"]]

                sessions[session_id] = FitnessSession(
                    session_id,
                    participant,
                )
            sessions[session_id].add_observation(observation)

    return sessions
