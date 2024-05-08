#from typing import Tuple
from skyfield.api import load
from skyfield.timelib import Timescale
from skyfield.vectorlib import VectorSum

class Coordinates:
    """Coordinates utility class"""

    def __init__(self) -> None:
        """Initialize the coordinates class, load the planets information, create earth and timescale"""
        self.planets = load("de421.bsp")
        self.earth = self.planets["earth"]
        self.moon = self.planets["moon"]
        self.ts = load.timescale()


    def dd2dms(self, dd: float) -> str:
        """Convert decimal degrees to a string (dd:mm:ss)

        Parameters:
        dd (float): The degrees to convert

        Returns:
        str: The degrees in human readable format
        """
        is_positive = dd >= 0
        dd = abs(dd)
        minutes, seconds = divmod(dd * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        sign = "+" if is_positive else "-"
        dms = "%s%02d:%02d:%02d" % (sign, degrees, minutes, seconds)
        return dms

    def dd2aligndms(self, dd: float) -> str:
        """Convert decimal degrees to a string (sDD*MM:SS)

        Parameters:
        dd (float): The degrees to convert

        Returns:
        str: The degrees in the format needed to send to the Nexus
        """
        is_positive = dd >= 0
        dd = abs(dd)
        minutes, seconds = divmod(dd * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        sign = "+" if is_positive else "-"
        dms = "%s%02d*%02d:%02d" % (sign, degrees, minutes, seconds)
        return dms

    def ddd2dms(self, dd: float) -> str:
        """Convert decimal degrees to a string (ddd:mm:ss)

        Parameters:
        dd (float): The degrees to convert

        Returns:
        str: The degrees in human readable format
        """
        minutes, seconds = divmod(dd * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        dms = "%03d:%02d:%02d" % (degrees, minutes, seconds)
        return dms

    def hh2dms(self, dd: float) -> str:
        """Convert decimal hours to a string (dd:mm:ss)

        Parameters:
        dd (float): The hours to convert

        Returns:
        str: The hours in human readable format (without sign)
        """
        minutes, seconds = divmod(dd * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        dms = "%02d:%02d:%02d" % (degrees, minutes, seconds)
        return dms

    def get_ts(self) -> Timescale:
        """Returns the timescale

        Returns:
        Timescale: The Timescale
        """
        return self.ts

    def get_earth(self) -> VectorSum:
        """Returns the earth object

        Returns:
        VectorSum: The VectorSum of the earth
        """
        return self.earth
    
    def get_moon(self) -> VectorSum:
        """Returns the moon object

        Returns:
        VectorSum: The VectorSum of the moon
        """
        return self.moon

    
