from src.models.wmm_model import WMMModel
import src.wmm_v2 as WMMv2
from src.utils.date_utils import DateUtils
from datetime import datetime, timedelta

class WMMCalculator:
    @staticmethod
    def calculate(model: WMMModel):
        decimal_year = DateUtils.decimal_year(model.year)
        dec = WMMv2.getDeclination(model.latitude, model.longitude, decimal_year, model.altitude)
        dip = WMMv2.getDipAngle(model.latitude, model.longitude, decimal_year, model.altitude)
        ti = WMMv2.getIntensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bh = WMMv2.getHorizontalIntensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bx = WMMv2.getNorthIntensity(model.latitude, model.longitude, decimal_year, model.altitude)
        by = WMMv2.getEastIntensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bz = WMMv2.getVerticalIntensity(model.latitude, model.longitude, decimal_year, model.altitude)
        model.set_results(dec, dip, ti, bh, bx, by, bz)

    @staticmethod
    def calculate_next_year(model: WMMModel):
        current_date = datetime.strptime(model.year, '%Y-%m-%d')
        next_date = current_date + timedelta(days=365)  # This doesn't account for leap years
        next_year = next_date.strftime('%Y-%m-%d')
        next_model = WMMModel(latitude=model.latitude,
                              longitude=model.longitude,
                              altitude=model.altitude,
                              year=next_year)

        WMMCalculator.calculate(next_model)
        return next_model

    @staticmethod
    def calculate_variation(model: WMMModel, next_model: WMMModel):
        variation = {
            "dec": next_model.dec - model.dec,
            "dip": next_model.dip - model.dip,
            "ti": next_model.ti - model.ti,
            "bh": next_model.bh - model.bh,
            "bx": next_model.bx - model.bx,
            "by": next_model.by - model.by,
            "bz": next_model.bz - model.bz
        }
        return variation