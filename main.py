from fitness_analyzer.csv_reader import load_participants, load_sessions
from fitness_analyzer.analysis import analyze_session
from fitness_analyzer.reports import (
    create_output_directory,
    write_analysis_summary,
    write_analysis_report,
    write_rejected_records,
)
import argparse

parser = argparse.ArgumentParser(
    description= "Smart Fitness Session Analyzer"
)

parser.add_argument(
    "--profiles",
    default="data/participants.csv",
)

parser.add_argument(
    "--sessions",
    default="data/fitness_sessions.csv",
)

parser.add_argument(
    "--invalid-sessions",
    default="data/fitness_sessions_invalid.csv",
)

parser.add_argument(
    "--output",
    default="output",
)

args = parser.parse_args()

try:
    participants = load_participants(args.profiles)
except FileNotFoundError as error:
    print(f"file not found: {error.filename}")
    raise SystemExit(1)

except PermissionError as error:
    print(f"Permission denied: {error.filename}")
    raise SystemExit(1)

valid_sessions, valid_rejected = load_sessions(
    args.sessions,
    participants,
)

invalid_sessions, invalid_rejected = load_sessions(
    args.invalid_sessions,
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

output_directory = create_output_directory(args.output)

write_analysis_summary(results, output_directory)
write_analysis_report(results, output_directory)
write_rejected_records(rejected_records, output_directory)


accepted_rows = sum(
    len(session.observations)
    for session in sessions.values()
)


print("\nProcessing complete")
print("Accepted rows:", accepted_rows)
print("Rejected rows:", len(rejected_records))
print("Created report files:")
print("- analysis_summary.csv")
print("- analysis_report.txt")
print("- rejected_records.txt")