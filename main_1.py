from space_network_lib import *
class Satellite(SpaceEntity):
    def __init__(self , name, distance_from_earth ):
        super().__init__(name, distance_from_earth)
    def receive_signal(self , packet):
        print(f" [{self.name}]Received: {packet}")

network = SpaceNetwork(level=1)
Sat1 = Satellite("Satellite_1", 100)
Sat2 = Satellite("Satellite_2", 200)

text = Packet("לווין" , Sat1, Sat2)
network.send(text)
