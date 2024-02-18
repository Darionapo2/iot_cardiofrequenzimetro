import json
import math
import random
import time


class CardiovascularTelemetry:
    heart_rate: int # [bpm] beats per minute
    oxygen_saturation: float # % of hemoglobin saturation

    def __init__(self, heart_rate: int = 100, oxygen_saturation: float = 1) -> None:
        self.heart_rate = heart_rate
        self.oxygen_saturation = oxygen_saturation

    def update_values_randomly(self) -> None:
        self.heart_rate = random.randint(65, 110)
        self.oxygen_saturation = round(random.uniform(0.95, 1), 3)

    def to_json(self) -> str:
        return json.dumps(self, default = lambda o: o.__dict__)



def main():
    ct = CardiovascularTelemetry(80, 0.97)
    while True:
        ct.update_values_randomly()
        print(ct.to_json())
        time.sleep(1)

if __name__ == '__main__':
    main()