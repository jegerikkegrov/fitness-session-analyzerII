def calculate_average(values):
    if not values:
        return None

    return sum(values) / len(values)

def analyze_session(session):
    observations = session.observations

    if len(observations) < 4:
        return {
            "session_id": session.session_id,
            "participant_id": session.participant.participant_id,
            "classification": "insufficient usable data",
            "reason": "Fewer than 4 usable observations"
        }

    heart_rate = [
        observation.heart_rate
        for observation in observations
    ]

    activity_levels = [
        observation.activity_level
        for observation in observations
    ]

    average_heart_rate = calculate_average(heart_rate)
    average_activity = calculate_average(activity_levels)

    baseline_heart_rate = (
        session.participant.reference_profile.baseline_heart_rate
    )

    heart_rate_difference = (
        average_heart_rate - baseline_heart_rate
    )

    if average_activity < 0.3 and heart_rate_difference < 20:
        classification = "resting"

    elif average_activity < 0.68 and heart_rate_difference < 50:
        classification = "moderate activity"

    else:
        classification = "high activity"

    first_observation = observations[0]
    last_observation = observations[-1]

    is_recovering = (
        last_observation.heart_rate < first_observation.heart_rate
        and last_observation.activity_level < first_observation.activity_level
    )

    return {
        "session_id": session.session_id,
        "participant_id": session.participant.participant_id,
        "average_heart_rate": average_heart_rate,
        "average_activity": average_activity,
        "heart_rate_difference": heart_rate_difference,
        "classification": classification,
        "recovering": is_recovering,
        "reason": (
            f"Average activity {average_activity:.2f}, "
            f"heart rate {heart_rate_difference:.1f} BPM "
            f"from personal baseline"
        )
    }



