
import time
from skyfield.api import Star, wgs84
#from datetime import datetime, timedelta
import os
import Display_64
import Coordinates_lite
from gps3 import agps3

class Geoloc:
    """The Geoloc utility class"""

    def __init__(self, handpad: Display_64, coordinates: Coordinates_lite) -> None:
        """Initializes

        Parameters:
        handpad (Display): The handpad that is connected to the eFinder
        coordinates (Coordinates): The coordinates utility class to be used in the eFinder
        """
        self.handpad = handpad
        self.aligned = False
        self.coordinates = coordinates
        self.long = 0
        self.lat = 0
        self.earth,self.moon = coordinates.get_earth(), coordinates.get_moon()
        self.ts = coordinates.get_ts()


    def getGps(self):
        gps_socket = agps3.GPSDSocket()
        data_stream = agps3.DataStream()
        gps_socket.connect()
        gps_socket.watch()
        for new_data in gps_socket:
            if new_data:
                print('trying for GPS Lock')
                self.handpad.display('Trying for','GPS Lock','')
                data_stream.unpack(new_data)
                if data_stream.mode == 3:
                    print('Geo data:',data_stream.time, data_stream.lon,data_stream.lat,data_stream.alt)
                    date = data_stream.time
                    lat = data_stream.lat
                    long = data_stream.lon
                    return (date,lat,long)

    def read(self) -> None:
        """Reads geodata from the GPS dongle"""
        
        dateTime,self.lat,self.long = self.getGps()
        print('Lat,Long', self.lat, self.long)
        self.location = self.coordinates.get_earth() + wgs84.latlon(self.lat, self.long)
        self.site = wgs84.latlon(self.lat,self.long)
        print('GPS reports UTC:',dateTime)
        dateTime = dateTime.replace('T',' ')
        dateTime = dateTime.replace('-','')
        print("setting pi clock to UTC")
        os.system('sudo date -u --set="%s"' % dateTime)
        self.handpad.display("GPS Data", "Acquired", "Datetime set")
        time.sleep(1)

    def altaz2Radec(self,az,alt):
        t = self.ts.now()
        a = self.location.at(t)
        pos = a.from_altaz(alt_degrees=alt,az_degrees=az)
        ra,dec,d = pos.radec()
        return ra.hours,dec.degrees
        
    def get_location(self):
        """Returns the location in space of the observer

        Returns:
        location: The location
        """
        return self.location
    
    def get_site(self):
        """Returns the location on earth of the observer

        Returns:
        location: The site
        """
        return self.site
    
    def get_long(self):
        """Returns the longitude of the observer

        Returns:
        long: The lonogitude
        """
        return self.long

    def get_lat(self):
        """Returns the latitude of the observer

        Returns:
        lat: The latitude
        """
        return self.lat
        
    def get_lunar_rates(self):
        t = self.ts.now()
        a = self.get_location().at(t).observe(self.moon).apparent()
        alt, az, distance, alt_rate, az_rate, range_rate = (a.frame_latlon_and_rates(self.site))
        ra,dec,d = a.radec()
        return (ra.hours,dec.degrees,alt.degrees,alt_rate.arcseconds.per_second,az_rate.arcseconds.per_second)
    
    def get_rate(self,ra,dec):
        t = self.ts.now()
        scope = Star(ra_hours = ra,dec_degrees = dec)
        a = self.get_location().at(t).observe(scope).apparent()
        alt, az, distance, alt_rate, az_rate, range_rate = (a.frame_latlon_and_rates(self.site))
        return (alt,az,alt_rate.arcseconds.per_second,az_rate.arcseconds.per_second)
