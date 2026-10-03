import csv
from pathlib import Path

from fitness_analyzer.models import (Participant, ReferenceProfile, Observation, FitnessSession)
from fitness_analyzer.validation import (
    validate_participant_id,
    validate_session_id,
    validate_heart_rate,
    validate_temperature,
    validate_activity_level,
    validate_signal_quality,
    validate_skin_response,
)
from fitness_analyzer.exceptions import InvalidIdentifierError

def add_rejection(rejected_records, file_path, row_number, field, reason):
    rejected_records.append({
        "sourse": Path(file_path).name,
        "row": row_number,
        "field": field,
        "reason": reason,
    })

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
    rejected_records = []

    with open(file_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            try:
                validate_session_id(row["session_id"])
            except InvalidIdentifierError as error:
                add_rejection(
                    rejected_records,
                    file_path,
                    row_number,
                    "session_id",
                    str(error)
                )
                continue
            try:
                validate_participant_id(row["participant_id"])
            except InvalidIdentifierError as error:
                add_rejection(
                    rejected_records,
                    file_path,
                    row_number,
                    "participant_id",
                    str(error)
                )
                continue

            if row["participant_id"] not in participants:
                add_rejection(
                    rejected_records,
                    file_path,
                    row_number,
                    "participant_id",
                    f"Unknown participant ID: {row['participant_id']}"
                )
                continue


            try:
                observation = Observation(
                    int(row["timestamp"]),
                    int(row["heart_rate"]),
                    float(row["skin_response"]),
                    float(row["temperature"]),
                    float(row["activity_level"]),
                    float(row["signal_quality"]),
                )
            except (ValueError, TypeError) as error:
                add_rejection(
                    rejected_records,
                    file_path,
                    row_number,
                    "Measurement",
                    f"invalid numeric value: {error}"
                )
                continue

            try:
                validate_heart_rate(observation.heart_rate)
                validate_skin_response(observation.skin_response)
                validate_temperature(observation.temperature)
                validate_activity_level(observation.activity_level)
                validate_signal_quality(observation.signal_quality)
            except ValueError as error:
                add_rejection(
                    rejected_records,
                    file_path,
                    row_number,
                    "measurement",
                    str(error)
                )
                continue

            session_id = row["session_id"]

            if session_id not in sessions:
                participant = participants[row["participant_id"]]

                sessions[session_id] = FitnessSession(
                    session_id,
                    participant,
                )
            sessions[session_id].add_observation(observation)

    return sessions, rejected_records

