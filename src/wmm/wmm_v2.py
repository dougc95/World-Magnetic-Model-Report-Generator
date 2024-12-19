import os
from .wmm_model import WorldMagneticModel

# Load the model once at import time
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "WMM.COF")

_wmm = WorldMagneticModel(DATA_FILE_PATH)

def get_declination(lat, lon, year, altitude):
    return _wmm.get_declination(lat, lon, year, altitude)

def get_dip_angle(lat, lon, year, altitude):
    return _wmm.get_dip_angle(lat, lon, year, altitude)

def get_intensity(lat, lon, year, altitude):
    return _wmm.get_intensity(lat, lon, year, altitude)

def get_horizontal_intensity(lat, lon, year, altitude):
    return _wmm.get_horizontal_intensity(lat, lon, year, altitude)

def get_north_intensity(lat, lon, year, altitude):
    return _wmm.get_north_intensity(lat, lon, year, altitude)

def get_east_intensity(lat, lon, year, altitude):
    return _wmm.get_east_intensity(lat, lon, year, altitude)

def get_vertical_intensity(lat, lon, year, altitude):
    return _wmm.get_vertical_intensity(lat, lon, year, altitude)
