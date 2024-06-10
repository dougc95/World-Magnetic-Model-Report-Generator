class WMMModel:
    def __init__(self, latitude, longitude, altitude, year):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.year = year
        self.dec = None
        self.dip = None
        self.by = None
        self.bh = None
        self.ti = None
        self.bx = None
        self.bz = None