from fitness_analyzer.csv_reader import load_participants, load_sessions

participants = load_participants("data/participants.csv")

sessions, rejected_records = load_sessions(
    "data/fitness_sessions_invalid.csv",
    participants,
)

print("Rejected records:", len(rejected_records))
for record in rejected_records:
    print(record)

print("Sessions loaded", len(sessions))

for session_id, session in sessions.items():
    print(
        session_id,
        "- Participant:",
        session.participant.participant_id,
        "- Observation:",
        len(session.observations),
    )

