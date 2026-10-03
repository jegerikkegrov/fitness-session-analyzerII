from fitness_analyzer.csv_reader import load_participants, load_sessions

participants = load_participants("data/participants.csv")

sessions = load_sessions(
    "data/fitness_sessions.csv",
    participants,
)

print("Sessions loaded", len(sessions))

for session_id, session in sessions.items():
    print(
        session_id,
        "- Participant:",
        session.participant.participant_id,
        "- Observation:",
        len(session.observations),
    )