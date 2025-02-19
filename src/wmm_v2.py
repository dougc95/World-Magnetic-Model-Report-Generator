import os
import math
import numpy as np

class WMMv2:
    _instance = None

    @classmethod
    def _get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # Model configuration (unchanged from old.py)
        self.maxdeg = 12
        self.maxord = self.maxdeg
        self.defaultDate = 2020.0

        # Magnetic field outputs (nT and degrees)
        self.dec = 0.0   # declination
        self.dip = 0.0   # dip angle
        self.ti = 0.0    # total intensity
        self.bx = 0.0    # north intensity
        self.by = 0.0    # east intensity
        self.bz = 0.0    # vertical intensity
        self.bh = 0.0    # horizontal intensity

        # Epoch and caching variables (for geodetic conversion)
        self.epoch = 0.0
        self.otime = self.oalt = self.olat = self.olon = -1000.0

        # WGS-84/IAU constants (unchanged)
        self.a = 6378.137
        self.b = 6356.7523142
        self.re = 6371.2
        self.a2 = self.a * self.a
        self.b2 = self.b * self.b
        self.c2 = self.a2 - self.b2
        self.a4 = self.a2 * self.a2
        self.b4 = self.b2 * self.b2
        self.c4 = self.a4 - self.b4

        # Allocate arrays as in old.py
        self.c    = [[0.0 for _ in range(13)] for _ in range(13)]
        self.cd   = [[0.0 for _ in range(13)] for _ in range(13)]
        self.tc   = [[0.0 for _ in range(13)] for _ in range(13)]
        self.dp   = [[0.0 for _ in range(13)] for _ in range(13)]
        self.snorm = np.zeros(169)  # 13x13 = 169 entries
        self.sp   = np.zeros(13)
        self.cp   = np.zeros(13)
        self.fn   = np.zeros(13)
        self.fm   = np.zeros(13)
        self.pp   = np.zeros(13)
        self.k    = [[0.0 for _ in range(13)] for _ in range(13)]

        # Variables used in the conversion from geodetic to spherical coordinates
        self.ct = 0.0
        self.st = 0.0
        self.r  = 0.0
        self.d  = 0.0
        self.ca = 0.0
        self.sa = 0.0

        # Load coefficients and perform normalization (unchanged logic)
        self.start()

    def start(self):
        # Initialization as in old.py
        self.maxord = self.maxdeg
        self.sp[0] = 0.0
        self.cp[0] = self.snorm[0] = self.pp[0] = 1.0
        self.dp[0][0] = 0.0

        # Read WMM.COF (adjust file_path as needed)
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "WMM.COF")
        with open(file_path, "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) == 1:
                    break
                if len(parts) == 3:
                    self.epoch = float(parts[0])
                    self.defaultDate = self.epoch + 2.5
                else:
                    n = int(parts[0])
                    m = int(parts[1])
                    gnm = float(parts[2])
                    hnm = float(parts[3])
                    dgnm = float(parts[4])
                    dhnm = float(parts[5])
                    if m <= n:
                        self.c[m][n] = gnm
                        self.cd[m][n] = dgnm
                        if m != 0:
                            self.c[n][m - 1] = hnm
                            self.cd[n][m - 1] = dhnm

        # Schmidt normalization factors (unchanged)
        self.snorm[0] = 1.0
        n = 1
        while n <= self.maxord:
            self.snorm[n] = self.snorm[n - 1] * (2 * n - 1) / n
            j = 2
            m = 0
            D1 = 1
            D2 = (n - m + D1) / D1
            while D2 > 0:
                self.k[m][n] = float(((n - 1)**2 - m**2)) / float((2 * n - 1) * (2 * n - 3))
                if m > 0:
                    flnmj = ((n - m + 1) * j) / float(n + m)
                    self.snorm[n + m * 13] = self.snorm[n + (m - 1) * 13] * math.sqrt(flnmj)
                    j = 1
                    self.c[n][m - 1] = self.snorm[n + m * 13] * self.c[n][m - 1]
                    self.cd[n][m - 1] = self.snorm[n + m * 13] * self.cd[n][m - 1]
                self.c[m][n] = self.snorm[n + m * 13] * self.c[m][n]
                self.cd[m][n] = self.snorm[n + m * 13] * self.cd[m][n]
                D2 = D2 - 1
                m = m + D1
            self.fn[n] = n + 1
            self.fm[n] = n
            n = n + 1
        self.k[1][1] = 0.0
        self.otime = self.oalt = self.olat = self.olon = -1000.0

    def _calculate_geomag(self, fLat, fLon, year, altitude=0):
        # This method contains the exact same mathematical logic as old.py
        self.glat = fLat
        self.glon = fLon
        self.alt = altitude
        self.time = year

        dt = self.time - self.epoch
        pi = math.pi
        dtr = pi / 180.0
        rlon = self.glon * dtr
        rlat = self.glat * dtr
        srlon = math.sin(rlon)
        srlat = math.sin(rlat)
        crlon = math.cos(rlon)
        crlat = math.cos(rlat)
        srlat2 = srlat * srlat
        crlat2 = crlat * crlat

        self.sp[1] = srlon
        self.cp[1] = crlon

        # Convert geodetic to spherical coordinates (only recalc if lat/alt changed)
        if altitude != self.oalt or fLat != self.olat:
            q = math.sqrt(self.a2 - self.c2 * srlat2)
            q1 = altitude * q
            q2 = ((q1 + self.a2) / (q1 + self.b2)) ** 2
            ct = srlat / math.sqrt(q2 * crlat2 + srlat2)
            st = math.sqrt(1.0 - ct * ct)
            r2 = altitude * altitude + 2.0 * q1 + (self.a4 - self.c4 * srlat2) / (q * q)
            r = math.sqrt(r2)
            d = math.sqrt(self.a2 * crlat2 + self.b2 * srlat2)
            ca = (altitude + d) / r
            sa = self.c2 * crlat * srlat / (r * d)
            self.ct = ct
            self.st = st
            self.r  = r
            self.d  = d
            self.ca = ca
            self.sa = sa
        else:
            ct = self.ct
            st = self.st
            r  = self.r
            d  = self.d
            ca = self.ca
            sa = self.sa

        if fLon != self.olon:
            m = 2
            while m <= self.maxord:
                self.sp[m] = self.sp[1] * self.cp[m - 1] + self.cp[1] * self.sp[m - 1]
                self.cp[m] = self.cp[1] * self.cp[m - 1] - self.sp[1] * self.sp[m - 1]
                m = m + 1

        aor = self.re / r
        ar = aor * aor
        br = 0.0
        bt = 0.0
        bp = 0.0
        bpp = 0.0

        n = 1
        while n <= self.maxord:
            ar = ar * aor
            m = 0
            D1 = 1
            D2 = (n + m + D1) / D1
            while D2 > 0:
                if altitude != self.oalt or fLat != self.olat:
                    if n == m:
                        self.snorm[n + m * 13] = st * self.snorm[n - 1 + (m - 1) * 13]
                        self.dp[m][n] = st * self.dp[m - 1][n - 1] + ct * self.snorm[n - 1 + (m - 1) * 13]
                    if n == 1 and m == 0:
                        self.snorm[n + m * 13] = ct * self.snorm[n - 1 + m * 13]
                        self.dp[m][n] = ct * self.dp[m][n - 1] - st * self.snorm[n - 1 + m * 13]
                    if n > 1 and n != m:
                        if m > n - 2:
                            self.snorm[n - 2 + m * 13] = 0.0
                            self.dp[m][n - 2] = 0.0
                        self.snorm[n + m * 13] = ct * self.snorm[n - 1 + m * 13] - self.k[m][n] * self.snorm[n - 2 + m * 13]
                        self.dp[m][n] = ct * self.dp[m][n - 1] - st * self.snorm[n - 1 + m * 13] - self.k[m][n] * self.dp[m][n - 2]
                self.tc[m][n] = self.c[m][n] + dt * self.cd[m][n]
                if m != 0:
                    self.tc[n][m - 1] = self.c[n][m - 1] + dt * self.cd[n][m - 1]
                par = ar * self.snorm[n + m * 13]
                if m == 0:
                    temp1 = self.tc[m][n] * self.cp[m]
                    temp2 = self.tc[m][n] * self.sp[m]
                else:
                    temp1 = self.tc[m][n] * self.cp[m] + self.tc[n][m - 1] * self.sp[m]
                    temp2 = self.tc[m][n] * self.sp[m] - self.tc[n][m - 1] * self.cp[m]
                bt = bt - ar * temp1 * self.dp[m][n]
                bp = bp + self.fm[m] * temp2 * par
                br = br + self.fn[n] * temp1 * par
                if st == 0.0 and m == 1:
                    if n == 1:
                        self.pp[n] = self.pp[n - 1]
                    else:
                        self.pp[n] = ct * self.pp[n - 1] - self.k[m][n] * self.pp[n - 2]
                    parp = ar * self.pp[n]
                    bpp = bpp + self.fm[m] * temp2 * parp
                D2 = D2 - 1
                m = m + D1
            n = n + 1

        if st == 0.0:
            bp = bpp
        else:
            bp = bp / st

        self.bx = -bt * ca - br * sa
        self.by = bp
        self.bz = bt * sa - br * ca

        self.bh = math.sqrt(self.bx * self.bx + self.by * self.by)
        self.ti = math.sqrt(self.bh * self.bh + self.bz * self.bz)

        self.dec = math.atan2(self.by, self.bx) / dtr
        self.dip = math.atan2(self.bz, self.bh) / dtr

        self.otime = self.time
        self.oalt = altitude
        self.olat = fLat
        self.olon = fLon

    @classmethod
    def get_declination(cls, dLat, dLong, year, altitude):
        inst = cls._get_instance()
        inst._calculate_geomag(dLat, dLong, year, altitude)
        return inst.dec

    @classmethod
    def get_dip_angle(cls, dLat, dLong, year, altitude):
        inst = cls._get_instance()
        inst._calculate_geomag(dLat, dLong, year, altitude)
        return inst.dip

    @classmethod
    def get_intensity(cls, dLat, dLong, year, altitude):
        inst = cls._get_instance()
        inst._calculate_geomag(dLat, dLong, year, altitude)
        return inst.ti

    @classmethod
    def get_horizontal_intensity(cls, dLat, dLong, year, altitude):
        inst = cls._get_instance()
        inst._calculate_geomag(dLat, dLong, year, altitude)
        return inst.bh

    @classmethod
    def get_north_intensity(cls, dLat, dLong, year, altitude):
        inst = cls._get_instance()
        inst._calculate_geomag(dLat, dLong, year, altitude)
        return inst.bx

    @classmethod
    def get_east_intensity(cls, dLat, dLong, year, altitude):
        inst = cls._get_instance()
        inst._calculate_geomag(dLat, dLong, year, altitude)
        return inst.by

    @classmethod
    def get_vertical_intensity(cls, dLat, dLong, year, altitude):
        inst = cls._get_instance()
        inst._calculate_geomag(dLat, dLong, year, altitude)
        return inst.bz
