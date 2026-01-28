import time
from space_network_lib import (
    SpaceNetwork, SpaceEntity, Packet,
    TemporalInterferenceError, DataCorruptedError,
    LinkTerminatedError, OutOfRangeError
)


class BrokenConnectionError(Exception):
    pass

class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(data=packet_to_relay, sender=sender, receiver=proxy)

    def __repr__(self):
        return f"Relay Packet (Relaying [{self.data}] to {self.receiver} from {self.sender})"
class Earth(SpaceEntity):
    def __init__(self, name, distance_from_earth=0):
        super().__init__(name, distance_from_earth)
    def receive_signal(self, packet: Packet):
        pass


class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        # בדיקה האם מדובר ב-Relay Packet [cite: 124-126]
        if isinstance(packet, RelayPacket):
            inner_packet = packet.data  # חילוץ הפקטה הפנימית [cite: 131]
            print(f"[{self.name}] Unwrapping and forwarding to {inner_packet.receiver.name}")
            # העברת הפקטה הפנימית ליעד [cite: 132]
            attempt_transmission(inner_packet)
        else:
            # הגעה ליעד הסופי [cite: 133-135]
            print(f"[{self.name}] Final destination reached: {packet.data}")

def attempt_transmission(packet):
    while True:
        try:
            network.send(packet)
            break
        except TemporalInterferenceError:
            print("...Interference, waiting")
            time.sleep(2)
        except DataCorruptedError:
            print("...corrupted, retrying")
        except (LinkTerminatedError, OutOfRangeError) as e:
            if isinstance(e, LinkTerminatedError):
                print("Link lost")
            else:
                print("Target out of range")
            raise BrokenConnectionError()

if __name__ == "__main__":
    network = SpaceNetwork(level=3)

    earth = Earth("Earth", 0)
    sat1 = Satellite("Sat1", 100)
    sat2 = Satellite("Sat2", 200)
    sat3 = Satellite("Sat3", 300)
    sat4 = Satellite("Sat4", 400)
    p_final = Packet("Hello From Earth!", sat3, sat4)
    p_to_sat3 = RelayPacket(p_final, sat2, sat3)
    p_to_sat2 = RelayPacket(p_to_sat3, sat1, sat2)
    p_onion = RelayPacket(p_to_sat2, earth, sat1)
    try:
        print(f"Sending onion packet: {p_onion}\n")
        attempt_transmission(p_onion)
    except BrokenConnectionError:
        print("Transmission failed")

print("")