import numpy as np

MAXDEG = 12
RE = 6371.2  # Mean radius of IAU-66 ellipsoid, in km
A = 6378.137  # Semi-major axis of WGS-84 ellipsoid, in km
B = 6356.7523142  # Semi-minor axis of WGS-84 ellipsoid, in km

A2 = A * A
B2 = B * B
C2 = A2 - B2
A4 = A2 * A2
B4 = B2 * B2
C4 = A4 - B4

DTR = np.pi / 180.0

# Data structure sizes based on MAXDEG.
ARRAY_SIZE = MAXDEG + 1

# Initialize coefficient arrays.
C = np.zeros((ARRAY_SIZE, ARRAY_SIZE), dtype=float)
CD = np.zeros((ARRAY_SIZE, ARRAY_SIZE), dtype=float)
TC = np.zeros((ARRAY_SIZE, ARRAY_SIZE), dtype=float)
DP = np.zeros((ARRAY_SIZE, ARRAY_SIZE), dtype=float)
SNORM = np.zeros((169,), dtype=float)
SP = np.zeros((ARRAY_SIZE,), dtype=float)
CP = np.zeros((ARRAY_SIZE,), dtype=float)
FN = np.zeros((ARRAY_SIZE,), dtype=float)
FM = np.zeros((ARRAY_SIZE,), dtype=float)
PP = np.zeros((ARRAY_SIZE,), dtype=float)
K = np.zeros((ARRAY_SIZE, ARRAY_SIZE), dtype=float)
