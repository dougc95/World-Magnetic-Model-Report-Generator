import math
import os
from .constants import (MAXDEG, RE, A2, B2, C2, A4, B4, C4, DTR,
                        C, CD, TC, DP, SNORM, SP, CP, FN, FM, PP, K)
from .model_reader import read_wmm_coefficients

class WorldMagneticModel:
    def __init__(self, data_file_path):
        self.epoch = 0.0
        self.default_date = 2020.0

        self.c = C
        self.cd = CD
        self.tc = TC
        self.dp = DP
        self.snorm = SNORM
        self.sp = SP
        self.cp = CP
        self.fn = FN
        self.fm = FM
        self.pp = PP
        self.k = K

        self.otime = self.oalt = self.olat = self.olon = -1000.0
        self.dec = self.dip = self.ti = self.bx = self.by = self.bz = self.bh = 0.0
        self.maxord = MAXDEG

        # Load data
        self._load_model(data_file_path)
        self._initialize_model()

    def _load_model(self, data_file_path):
        self.epoch, coeff_data = read_wmm_coefficients(data_file_path)
        self.default_date = self.epoch + 2.5

        for (n, m, gnm, hnm, dgnm, dhnm) in coeff_data:
            if m <= n:
                self.c[m][n] = gnm
                self.cd[m][n] = dgnm
                if m != 0:
                    self.c[n][m-1] = hnm
                    self.cd[n][m-1] = dhnm

    def _initialize_model(self):
        self.sp[0] = 0.0
        self.cp[0] = self.snorm[0] = self.pp[0] = 1.0
        self.dp[0][0] = 0.0

        for n in range(1, self.maxord + 1):
            self.snorm[n] = self.snorm[n - 1] * ((2 * n - 1) / n)
            self.fn[n] = n + 1
            self.fm[n] = n

        for n in range(1, self.maxord + 1):
            for m in range(n + 1):
                if n == m:
                    self.k[m][n] = ((n-1)**2 - m*m) / ((2*n - 1)*(2*n - 3)) if n > 1 else 0.0
                else:
                    self.k[m][n] = ((n-1)**2 - m*m) / ((2*n - 1)*(2*n - 3))

                if m != 0:
                    flnmj = ((n - m + 1) * 1.0) / (n + m)
                    self.snorm[n + m*13] = self.snorm[n + (m-1)*13] * math.sqrt(flnmj)
                    self.c[n][m-1] *= self.snorm[n + m*13]
                    self.cd[n][m-1] *= self.snorm[n + m*13]

                self.c[m][n] *= self.snorm[n + m*13]
                self.cd[m][n] *= self.snorm[n + m*13]

        self.k[1][1] = 0.0

    def _calculate_geomag(self, glat, glon, time, alt):
        dt = time - self.epoch
        rlon = glon * DTR
        rlat = glat * DTR
        srlon = math.sin(rlon)
        srlat = math.sin(rlat)
        crlon = math.cos(rlon)
        crlat = math.cos(rlat)

        srlat2 = srlat*srlat
        crlat2 = crlat*crlat
        self.sp[1] = srlon
        self.cp[1] = crlon

        if alt != self.oalt or glat != self.olat:
            q = math.sqrt(A2 - C2 * srlat2)
            q1 = alt * q
            q2 = ((q1 + A2)/(q1 + B2))**2
            ct = srlat / math.sqrt(q2*crlat2 + srlat2)
            st = math.sqrt(1.0 - ct*ct)
            r2 = alt*alt + 2.0*q1 + (A4 - C4*srlat2)/(q*q)
            r = math.sqrt(r2)
            d = math.sqrt(A2*crlat2 + B2*srlat2)
            ca = (alt + d)/r
            sa = (C2*crlat*srlat)/(r*d)
            self._ct = ct
            self._st = st
            self._r = r
            self._ca = ca
            self._sa = sa
        else:
            ct = self._ct
            st = self._st
            r = self._r
            ca = self._ca
            sa = self._sa

        if glon != self.olon:
            for m in range(2, self.maxord+1):
                self.sp[m] = self.sp[1]*self.cp[m-1] + self.cp[1]*self.sp[m-1]
                self.cp[m] = self.cp[1]*self.cp[m-1] - self.sp[1]*self.sp[m-1]

        aor = RE/r
        ar = aor*aor
        br = bt = bp = bpp = 0.0

        for n in range(1, self.maxord+1):
            ar *= aor
            for m in range(n+1):
                if alt != self.oalt or glat != self.olat:
                    if n == m:
                        if n > 1:
                            self.snorm[n+m*13] = st*self.snorm[n-1+(m-1)*13]
                            self.dp[m][n] = st*self.dp[m-1][n-1] + ct*self.snorm[n-1+(m-1)*13]
                        else:
                            self.snorm[n+m*13] = ct*self.snorm[n-1+m*13]
                            self.dp[m][n] = ct*self.dp[m][n-1] - st*self.snorm[n-1+m*13]
                    elif n > 1 and n != m:
                        if m > n-2:
                            self.snorm[n-2+m*13] = 0.0
                            self.dp[m][n-2] = 0.0
                        self.snorm[n+m*13] = ct*self.snorm[n-1+m*13] - self.k[m][n]*self.snorm[n-2+m*13]
                        self.dp[m][n] = ct*self.dp[m][n-1] - st*self.snorm[n-1+m*13] - self.k[m][n]*self.dp[m][n-2]

                if time != self.otime:
                    self.tc[m][n] = self.c[m][n] + dt*self.cd[m][n]
                    if m != 0:
                        self.tc[n][m-1] = self.c[n][m-1] + dt*self.cd[n][m-1]

                par = ar*self.snorm[n+m*13]
                if m == 0:
                    temp1 = self.tc[m][n]*self.cp[m]
                    temp2 = self.tc[m][n]*self.sp[m]
                else:
                    temp1 = self.tc[m][n]*self.cp[m] + self.tc[n][m-1]*self.sp[m]
                    temp2 = self.tc[m][n]*self.sp[m] - self.tc[n][m-1]*self.cp[m]

                bt -= ar*temp1*self.dp[m][n]
                bp += (m*temp2*par)
                br += ((n+1)*temp1*par)

                if st == 0.0 and m == 1:
                    if n == 1:
                        self.pp[n] = self.pp[n-1]
                    else:
                        self.pp[n] = ct*self.pp[n-1] - self.k[m][n]*self.pp[n-2]
                    parp = ar*self.pp[n]
                    bpp += m*temp2*parp

        if st == 0.0:
            bp = bpp
        else:
            bp = bp/st

        self.bx = -bt*ca - br*sa
        self.by = bp
        self.bz = bt*sa - br*ca

        self.bh = math.sqrt(self.bx*self.bx + self.by*self.by)
        self.ti = math.sqrt(self.bh*self.bh + self.bz*self.bz)
        self.dec = math.atan2(self.by, self.bx)/DTR
        self.dip = math.atan2(self.bz, self.bh)/DTR

        self.otime = time
        self.oalt = alt
        self.olat = glat
        self.olon = glon

    def get_declination(self, lat, lon, year, altitude):
        self._calculate_geomag(lat, lon, year, altitude)
        return self.dec

    def get_dip_angle(self, lat, lon, year, altitude):
        self._calculate_geomag(lat, lon, year, altitude)
        return self.dip

    def get_intensity(self, lat, lon, year, altitude):
        self._calculate_geomag(lat, lon, year, altitude)
        return self.ti

    def get_horizontal_intensity(self, lat, lon, year, altitude):
        self._calculate_geomag(lat, lon, year, altitude)
        return self.bh

    def get_north_intensity(self, lat, lon, year, altitude):
        self._calculate_geomag(lat, lon, year, altitude)
        return self.bx

    def get_east_intensity(self, lat, lon, year, altitude):
        self._calculate_geomag(lat, lon, year, altitude)
        return self.by

    def get_vertical_intensity(self, lat, lon, year, altitude):
        self._calculate_geomag(lat, lon, year, altitude)
        return self.bz
