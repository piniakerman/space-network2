import time
from space_network_lib import SpaceNetwork, SpaceEntity, Packet, TemporalInterferenceError, DataCorruptedError


class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"[{self.name}] Received: {packet}. [cite: 69]")


def attempt_transmission(packet):
    while True:
        try:
            network.send(packet)
            break

        except TemporalInterferenceError:
            print("...Interference, waiting [cite: 15]")
            time.sleep(2)

        except DataCorruptedError:
            print("...corrupted, retrying [cite: 20]")


if __name__ == "__main__":
    network = SpaceNetwork(level=2)

    sat1 = Satellite("Sat1", 100)
    sat2 = Satellite("Sat2", 200)

    test_packet = Packet("Hello Space!", sat1, sat2)

    attempt_transmission(test_packet)