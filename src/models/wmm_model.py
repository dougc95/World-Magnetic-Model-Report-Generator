class WMMModel:
    def __init__(self, latitude, longitude, altitude, year):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.year = year
        self.dec = None
        self.dip = None
        self.ti = None
        self.bh = None
        self.bx = None
        self.by = None
        self.bz = None

    def __str__(self):
        return f"WMMModel(latitude={self.latitude}, longitude={self.longitude}, altitude={self.altitude}, year={self.year})"

    def __repr__(self):
        return self.__str__()

    def set_results(self, dec, dip, ti, bh, bx, by, bz):
        self.dec = dec
        self.dip = dip
        self.ti = ti
        self.bh = bh
        self.bx = bx
        self.by = by
        self.bz = bz

    def get_results(self):
        return {
            "dec": self.dec,
            "dip": self.dip,
            "ti": self.ti,
            "bh": self.bh,
            "bx": self.bx,
            "by": self.by,
            "bz": self.bz
        }