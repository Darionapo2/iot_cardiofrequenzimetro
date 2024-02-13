import json

class CardiovascularTelemetry:
    heart_rate: float # [bpm] beats per minute
    oxygen_saturation: float # % of hemoglobin saturation

    def __init__(self, heart_rate: float, oxygen_saturation: float) -> None:
        self.heart_rate = heart_rate
        self.oxygen_saturation = oxygen_saturation

    def to_json(self) -> str:
        return json.dumps(self, default = lambda o: o.__dict__)