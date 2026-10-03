from fitness_analyzer.csv_reader import load_participants, load_sessions
from fitness_analyzer.analysis import analyze_session
from fitness_analyzer.reports import (
    create_output_directory,
    write_analysis_summary,
    write_analysis_report,
    write_rejected_records,
)

participants = load_participants("data/participants.csv")

valid_sessions, valid_rejected = load_sessions(
    "data/fitness_sessions.csv",
    participants,
)

invalid_sessions, invalid_rejected = load_sessions(
    "data/fitness_sessions_invalid.csv",
    participants
)

sessions = {}
sessions.update(valid_sessions)
sessions.update(invalid_sessions)

rejected_records = valid_rejected + invalid_rejected


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

print("\nAnalysis results:")

results = []

for session in sessions.values():
    result = analyze_session(session)
    results.append(result)
    print(result)

output_directory = create_output_directory("output")

write_analysis_summary(results, output_directory)
write_analysis_report(results, output_directory)
write_rejected_records(rejected_records, output_directory)
