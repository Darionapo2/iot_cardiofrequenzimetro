import json
import time


class CardiovascularMonitoringWearable:
    uuid: str
    manufacturer: str
    model: str
    owner_id: str

    def __init__(self, uuid: str, manufacturer: str, model: str, owner_id: str) -> None:
        self.uuid = uuid
        self.manufacturer = manufacturer
        self.model = model
        self.owner_id = owner_id

    def to_json(self) -> str:
        return json.dumps(self, default = lambda o: o.__dict__)

def main():
    CMW = CardiovascularMonitoringWearable('12345', 'dario\'s ltd', 'pro', 'dario')
    print(CMW.to_json())

if __name__ == '__main__':
    main()