import time
from space_network_lib import (
    SpaceNetwork, SpaceEntity, Packet,
    TemporalInterferenceError, DataCorruptedError,
    LinkTerminatedError, OutOfRangeError
)


class BrokenConnectionError(Exception):
    pass


class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"[{self.name}] Received: {packet}.")


def attempt_transmission(packet):
    while True:
        try:
            network.send(packet)
            print("Transmission successful!")
            break

        except TemporalInterferenceError:
            print("...Interference, waiting")
            time.sleep(2)
        except DataCorruptedError:
            print("...corrupted, retrying")

        except LinkTerminatedError:
            print("Link lost")
            raise BrokenConnectionError("Permanent link failure")
        except OutOfRangeError:
            print("Target out of range")
            raise BrokenConnectionError("Target unreachable")


if __name__ == "__main__":
    network = SpaceNetwork(level=3)

    sat1 = Satellite("Sat1", 100)
    sat2 = Satellite("Sat2", 300)

    test_packet = Packet("Important Data", sat1, sat2)

    try:
        attempt_transmission(test_packet)
    except BrokenConnectionError:
        print("Transmission failed")