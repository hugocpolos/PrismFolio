class TargetParticipation:
    def __init__(self, target_participation: float):
        if not isinstance(target_participation, float):
            raise TypeError(
                f"Participation should be a float value. Received {target_participation}")

        if target_participation < 0:
            raise ValueError("Participation should not be a negative value. "
                             f"Received {target_participation}")

        if target_participation == 0.0:
            raise ValueError("Participation should not be zero.")

        if target_participation > 100.0:
            raise ValueError(f"Participation value should not be higher than 100%. "
                             f"Received {target_participation}.")
        self.__target_participation = target_participation

    # Public
    def get_target_participation(self):
        return self.__target_participation
