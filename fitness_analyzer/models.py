class ReferenceProfile:
    def __init__(
            self,
            baseline_heart_rate,
            baseline_skin_rate,
            baseline_temperature,
    ):
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_rate = baseline_skin_rate
        self.baseline_temperature = baseline_temperature

class Participant:
    def __init__(self, participant_id, reference_profile):
        self.participant_id = participant_id
        self.reference_profile = reference_profile

class Observation:
    def __init__(
            self,
            timestamp,
            heart_rate,
            skin_response,
            temperature,
            activity_level,
            signal_quality
    ):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

class FitnessSession:
    def __init__(
            self,
            session_id,
            participant,
    ):
        self.session_id = session_id
        self.participant = participant
        self._observations = []

    def add_observation(self, observation):
        self._observations.append(observation)

    @property
    def observations(self):
        return self._observations.copy()


