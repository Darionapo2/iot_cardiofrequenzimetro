import json

class StatusTelemetry:
    battery_level: float # % of battery charge
    emergency: bool # True when a cardiovascular anomaly is detected

    def __init__(self, battery_level: float) -> None:
        self.battery_level = battery_level
        self.emergency = False

    def to_json(self) -> str:
        return json.dumps(self, default = lambda o: o.__dict__)