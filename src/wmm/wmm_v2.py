import os
import numpy as np
import math

# Geodetic altitude in km
alt = 0
# Geodetic longitud in deg
glat = 0
# Geodetic latitude in deg
glon = 0
# Time in decimal years
time = 0

# -------------------------------
# Geomagnetic declination in deg
# East is + && West is -
dec = 0
# Geomagnetic inclination in deg
# Down is + && Up is -
dip = 0
# Total intensity in nanoTesla(nT)
ti = 0
# Grid variation referenced to grid North
# Not calculated
# gv=0
# -------------------------------

# Maximum number of degrees
maxdeg = 12
# Maximum order of spherical harmonic model
maxord = 0
# Default date
defaultDate = 2020.0
# Default altitude
defaultAltitude = 0

# --------------------------------
# Default coeficients of main magnetic model (nT)
c = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# Default coeficients of secular magnetic model (nT/yr)
cd = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# The time adjusted geomagnetic gauss coefficients (nt)
tc = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# The theta derivative of p(n,m) (unnormalized)
dp = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# The Schmidt normalization factors.
snorm = np.zeros(169)
# The sine of (m*spherical coord. longitude)
sp = np.zeros(13)
# The cosine of (m*spherical coord. longitude).
cp = np.zeros(13)
fn = np.zeros(13)
fm = np.zeros(13)
# The associated Legendre polynomials for m=1 (unnormalized).
pp = np.zeros(13)
k = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# -----------------------------------

# Variables para guardar datos en caso de no existir datos
otime, oalt, olat, olon = 0, 0, 0, 0
# Epochs
epoch = 0

# 	  *	 bx is the north south field intensity
#     *  by is the east west field intensity
#     *  bz is the vertical field intensity positive downward
#     *  bh is the horizontal field intensity
bx, by, bz, bh = 0, 0, 0, 0

#     *	re is the Mean radius of IAU-66 ellipsoid, in km.
#     *  a2 is the Semi-major axis of WGS-84 ellipsoid, in km, squared.
#     *  b2 is the Semi-minor axis of WGS-84 ellipsoid, in km, squared.
#     *  c2 is c2 = a2 - b2
#     *  a4 is a2 squared.
#     *  b4 is b2 squared.
#     *  c4 is c4 = a4 - b4
re, a2, b2, c2, a4, b4, c4 = 0, 0, 0, 0, 0, 0, 0

# It only calculates in one function
# These only recalculate if the altitude changes
r, d, ca, sa, ct, st = 0, 0, 0, 0, 0, 0


def start():
    global otime, oalt, olat, olon
    global c, cd, tc, dp, snorm, sp, cp, fn, fm, pp, k
    global glat
    global glon
    global maxord
    global dec, dip, ti
    global bx, by, bz, bh
    maxord = maxdeg
    sp[0] = 0.0
    cp[0] = snorm[0] = pp[0] = 1.0
    dp[0][0] = 0
    # Semi-major axis of WGS-84 ellipsoid, in km
    global a
    a = 6378.137
    # Semi-minor axis of WGS-84 ellipsoid, in km.
    global b
    b = 6356.7523142
    # Mean radius of IAU-66 ellipsoid, in km.
    global re, a2, b2, c2, a4, b4, c4
    global r, d, ca, sa, ct, st
    re = 6371.2
    a2 = a * a
    b2 = b * b
    c2 = a2 - b2
    a4 = a2 * a2
    b4 = b2 * b2
    c4 = a4 - b4
    # Lectura Archivo
    snorm[0] = 1.0
    n = 1
    while n <= maxord:
        n = n + 1
    file_path = os.path.join(os.path.dirname(__file__), "..", '..', "data", "WMM.COF")

    f = open(file_path, "r")
    for x in f:
        aux = x.split(" ")
        i = 0
        length = len(aux)
        aux1 = []
        for y in aux:
            if y != "":
                aux1.append(y)

        if len(aux1) == 1:
            break
            pass
        else:
            if len(aux1) == 3:
                global epoch
                epoch = float(aux1[0])
                defaultDate = epoch + 2.5
                pass
            else:
                n = int(aux1[0])
                m = int(aux1[1])
                gnm = float(aux1[2])
                hnm = float(aux1[3])
                dgnm = float(aux1[4])
                dhnm = float(aux1[5])

                if m <= n:
                    c[m][n] = gnm
                    cd[m][n] = dgnm
                    if m != 0:
                        c[n][m - 1] = hnm
                        cd[n][m - 1] = dhnm

    f.close()

    # Convert Schmidt normalized gauss Coefficientes to unnormalized
    snorm[0] = 1.0
    # for n in range(1,n<=maxord,1):
    n = 1
    while n <= maxord:
        snorm[n] = snorm[n - 1] * (2 * n - 1) / n
        j = 2
        # Translate the Java for loop with multiple instance with a while
        m, D1 = 0, 1
        D2 = (n - m + D1) / D1
        while D2 > 0:
            k[m][n] = float(((n - 1) * (n - 1)) - (m * m)) / float(
                (2 * n - 1) * (2 * n - 3)
            )
            if m > 0:
                flnmj = ((n - m + 1) * j) / float(n + m)
                vasoAuxiliar = math.sqrt(flnmj)
                snorm[n + m * 13] = snorm[n + (m - 1) * 13] * math.sqrt(flnmj)
                j = 1
                c[n][m - 1] = snorm[n + m * 13] * c[n][m - 1]
                cd[n][m - 1] = snorm[n + m * 13] * cd[n][m - 1]
                pass
            c[m][n] = snorm[n + m * 13] * c[m][n]
            cd[m][n] = snorm[n + m * 13] * cd[m][n]
            D2 = D2 - 1
            m = m + D1
            pass  # End while m
        fn[n] = n + 1
        fm[n] = n
        # print(snorm[n])
        n = n + 1
        # End for n
    k[1][1] = 0.0
    otime = oalt = olat = olon = -1000.0

    pass


start()


def calculate_geomag(fLat, fLon, year, altitude):
    global re, a2, b2, c2, a4, b4, c4
    global r, d, ca, sa, ct, st

    global c, cd, tc, dp, snorm, sp, cp, fn, fm, pp, k

    global dec, dip, ti
    global bx, by, bz, bh
    glat = fLat
    glon = fLon
    alt = altitude
    time = year
    # Calc
    dt = time - epoch
    # Ctte
    pi = math.pi
    dtr = pi / 180.0
    rlon = glon * dtr
    rlat = glat * dtr
    srlon = math.sin(rlon)
    srlat = math.sin(rlat)
    crlon = math.cos(rlon)
    crlat = math.cos(rlat)
    srlat2 = srlat * srlat
    crlat2 = crlat * crlat
    sp[1] = srlon
    cp[1] = crlon
    # Conversion Geodetic Coord TO Spherical Coord
    global oalt, olat, olon, otime
    if alt != oalt or glat != olat:
        q = math.sqrt(a2 - c2 * srlat2)
        q1 = alt * q
        q2 = ((q1 + a2) / (q1 + b2)) * ((q1 + a2) / (q1 + b2))
        ct = srlat / math.sqrt(q2 * crlat2 + srlat2)
        st = math.sqrt(1.0 - (ct * ct))
        r2 = (alt * alt) + 2.0 * q1 + (a4 - c4 * srlat2) / (q * q)
        r = math.sqrt(r2)
        d = math.sqrt(a2 * crlat2 + b2 * srlat2)
        ca = (alt + d) / r
        sa = c2 * crlat * srlat / (r * d)
        pass
    if glon != olon:
        m = 2
        while m <= maxord:
            sp[m] = sp[1] * cp[m - 1] + cp[1] * sp[m - 1]
            cp[m] = cp[1] * cp[m - 1] - sp[1] * sp[m - 1]
            m = m + 1
            pass
        pass
    aor = re / r
    ar = aor * aor
    br = 0
    bt = 0
    bp = 0
    bpp = 0
    n = 1
    while n <= maxord:
        ar = ar * aor
        m = 0
        D3 = 1
        D4 = (n + m + D3) / D3
        # Translate for (int m = 0,D3 = 1,D4 = (n + m + D3) / D3; D4 > 0; D4--,m += D3) TO while
        while D4 > 0:
            # COMPUTE UNNORMALIZED ASSOCIATED LEGENDRE POLYNOMIALS AND DERIVATIVES VIA RECURSION RELATIONS
            if alt != oalt or glat != olat:
                if n == m:
                    snorm[n + m * 13] = st * snorm[n - 1 + (m - 1) * 13]
                    dp[m][n] = st * dp[m - 1][n - 1] + ct * snorm[n - 1 + (m - 1) * 13]
                    pass
                if n == 1 and m == 0:
                    snorm[n + m * 13] = ct * snorm[n - 1 + m * 13]
                    dp[m][n] = ct * dp[m][n - 1] - st * snorm[n - 1 + m * 13]
                    pass
                if n > 1 and n != m:
                    if m > n - 2:
                        snorm[n - 2 + m * 13] = 0.0
                        dp[m][n - 2] = 0.0
                        pass
                    snorm[n + m * 13] = (
                        ct * snorm[n - 1 + m * 13] - k[m][n] * snorm[n - 2 + m * 13]
                    )
                    dp[m][n] = (
                        ct * dp[m][n - 1]
                        - st * snorm[n - 1 + m * 13]
                        - k[m][n] * dp[m][n - 2]
                    )
                    pass
                pass
            pass

            # TIME ADJUST THE GAUSS COEFFICIENTS
            if time != otime:
                tc[m][n] = c[m][n] + dt * cd[m][n]
                if m != 0:
                    tc[n][m - 1] = c[n][m - 1] + dt * cd[n][m - 1]
                    pass
                pass
            # ACCUMULATE TERMS OF THE SPHERICAL HARMONIC EXPANSIONS
            temp1, temp2 = 0, 0
            par = ar * snorm[n + m * 13]

            if m == 0:
                temp1 = tc[m][n] * cp[m]
                temp2 = tc[m][n] * sp[m]
            else:
                temp1 = tc[m][n] * cp[m] + tc[n][m - 1] * sp[m]
                temp2 = tc[m][n] * sp[m] - tc[n][m - 1] * cp[m]

            bt = bt - ar * temp1 * dp[m][n]
            bp += fm[m] * temp2 * par
            br += fn[n] * temp1 * par

            # SPECIAL CASE:  NORTH/SOUTH GEOGRAPHIC POLES
            if st == 0.0 and m == 1:
                if n == 1:
                    pp[n] = pp[n - 1]
                else:
                    pp[n] = ct * pp[n - 1] - k[m][n] * pp[n - 2]
                parp = ar * pp[n]
                bpp += fm[m] * temp2 * parp
                pass
            D4 = D4 - 1
            m = m + D3
            # End of for m
        n = n + 1
        # End of for n
    if st == 0.0:
        bp = bpp
    else:
        bp = bp / st  #!!!!WATCH
        pass
    pass

    """
	ROTATE MAGNETIC VECTOR COMPONENTS FROM SPHERICAL TO
	GEODETIC COORDINATES
	by is the east-west field component
	bx is the north-south field component
	bz is the vertical field component.
	"""

    bx = -bt * ca - br * sa
    by = bp
    bz = bt * sa - br * ca

    # Critical part
    bh = math.sqrt((bx * bx) + (by * by))
    ti = math.sqrt((bh * bh) + (bz * bz))
    # //	Calculate the declination.
    dec = math.atan2(by, bx) / dtr
    dip = math.atan2(bz, bh) / dtr

    otime = time
    oalt = alt
    olat = glat
    olon = glon


def get_declination(dLat, dLong, year, altitude):
    global dec
    calculate_geomag(dLat, dLong, year, altitude)
    return dec


def get_intensity(dLat, dLong, year, altitude):
    calculate_geomag(dLat, dLong, year, altitude)
    return ti


def get_horizontal_intensity(dLat, dLong, year, altitude):
    calculate_geomag(dLat, dLong, year, altitude)
    return bh


def get_vertical_intensity(dLat, dLong, year, altitude):
    calculate_geomag(dLat, dLong, year, altitude)
    return bz


def get_north_intensity(dLat, dLong, year, altitude):
    calculate_geomag(dLat, dLong, year, altitude)
    return bx


def get_east_intensity(dLat, dLong, year, altitude):
    calculate_geomag(dLat, dLong, year, altitude)
    return by


def get_dip_angle(dLat, dLong, year, altitude):
    calculate_geomag(dLat, dLong, year, altitude)
    return dip
