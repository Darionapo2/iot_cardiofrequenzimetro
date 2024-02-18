import json
import random
import time


class StatusTelemetry:
    battery_level: float # % of battery charge
    emergency: bool # True when a cardiovascular anomaly is detected

    def __init__(self, battery_level: float) -> None:
        self.battery_level = battery_level
        self.emergency = False

    def simulate_battery_discharge(self) -> None:
        self.battery_level -= round(random.uniform(1, 5), 2)

    def to_json(self) -> str:
        return json.dumps(self, default = lambda o: o.__dict__)


def main():
    st = StatusTelemetry(battery_level = 80)
    while True:
        st.simulate_battery_discharge()
        print(st.to_json())
        time.sleep(1)

if __name__ == '__main__':
    main()