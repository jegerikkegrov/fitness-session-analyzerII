import re

from fitness_analyzer.exceptions import InvalidIdentifierError

def validate_participant_id(participant_id):
    pattern = r"^P\d{3}$"

    if re.fullmatch(pattern, participant_id) is None:
        raise InvalidIdentifierError(f"Invalid participant ID: {participant_id}")

    return True

def validate_session_id(session_id):
    pattern = r"^FIT-\d{4}-\d{3}$"

    if re.fullmatch(pattern, session_id) is None:
        raise InvalidIdentifierError(f"Invalid session ID: {session_id}")

    return True

def validate_heart_rate(heart_rate):
    if heart_rate < 35 or heart_rate > 205:
        raise ValueError(
            f"Heart rate out of range: {heart_rate}"
        )

    return True

def validate_temperature(temperature):
    if temperature < 25 or temperature > 42:
        raise ValueError(
            f"Temperature out of range: {temperature}"
        )
    return True

def validate_activity_level(activity_level):
    if activity_level < 0 or activity_level > 1:
        raise ValueError(
            f"Activity level out of range: {activity_level}"
        )
    return True

def validate_skin_response(skin_response):
    if skin_response < 0:
        raise ValueError(
            f"Skin response out of range: {skin_response}"
        )
    return True

def validate_signal_quality(signal_quality):
    if signal_quality < 0 or signal_quality > 1:
        raise ValueError(
            f"Signal quality out of range: {signal_quality}"
        )

    if signal_quality < 0.5:
        raise ValueError(
            f"Signal quality too low: {signal_quality}"
        )

    return True

def validate_timestamp(timestamp):
    if timestamp < 0:
        raise ValueError(
            f"Timestamp cannot be negative: {timestamp}"
        )
    return True


