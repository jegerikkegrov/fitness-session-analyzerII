from fitness_analyzer.csv_reader import load_participants

participants = load_participants("data/participants.csv")

print("Participants: loaded:", len(participants))

for participant_id in participants:
    print(participant_id)