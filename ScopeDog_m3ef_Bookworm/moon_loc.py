import Nexus
import Display
import Coordinates

version = "1"
handpad = Display.Handpad(version)
coordinates = Coordinates.Coordinates()
nexus = Nexus.Nexus(handpad,coordinates)
nexus.read()
print(nexus.get_lunar_rates())