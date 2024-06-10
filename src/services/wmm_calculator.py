from src.models.wmm_model import WMMModel
from src.wmm_v2 import WMMv2

class WMMCalculator:
    @staticmethod
    def calculate(model: WMMModel):
        model.dec = WMMv2.getDeclination(model.latitude, model.longitude, model.year, model.altitude)
        model.dip = WMMv2.getDipAngle(model.latitude, model.longitude, model.year, model.altitude)
        model.by = WMMv2.getEastIntensity(model.latitude, model.longitude, model.year, model.altitude)
        model.bh = WMMv2.getHorizontalIntensity(model.latitude, model.longitude, model.year, model.altitude)
        model.ti = WMMv2.getIntensity(model.latitude, model.longitude, model.year, model.altitude)
        model.bx = WMMv2.getNorthIntensity(model.latitude, model.longitude, model.year, model.altitude)
        model.bz = WMMv2.getVerticalIntensity(model.latitude, model.longitude, model.year, model.altitude)