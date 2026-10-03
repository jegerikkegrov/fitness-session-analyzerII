import csv
from fitness_analyzer.models import Participant, ReferenceProfile
from fitness_analyzer.validation import validate_participant_id
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


