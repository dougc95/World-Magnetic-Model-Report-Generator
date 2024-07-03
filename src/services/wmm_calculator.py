import calendar
import src.wmm_v2 as WMMv2
from src.models.wmm_model import WMMModel
from src.utils.date_utils import DateUtils
from datetime import datetime, timedelta

class WMMCalculator:
    @staticmethod
    def calculate(model: WMMModel):
        decimal_year = DateUtils.decimal_year(model.year)
        dec = WMMv2.get_declination(model.latitude, model.longitude, decimal_year, model.altitude)
        dip = WMMv2.get_dip_angle(model.latitude, model.longitude, decimal_year, model.altitude)
        ti = WMMv2.get_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bh = WMMv2.get_horizontal_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bx = WMMv2.get_north_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        by = WMMv2.get_east_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bz = WMMv2.get_vertical_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        model.set_results(dec, dip, ti, bh, bx, by, bz)

    @staticmethod
    def calculate_next_year(model: WMMModel):
        current_date = datetime.strptime(model.year, "%Y-%m-%d")
        next_date = current_date + timedelta( 366 if calendar.isleap(model.year) else 365 )
        next_year = next_date.strftime("%Y-%m-%d")
        next_model = WMMModel(
            latitude=model.latitude,
            longitude=model.longitude,
            altitude=model.altitude,
            year=next_year,
        )

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