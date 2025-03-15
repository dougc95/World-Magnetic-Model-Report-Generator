from pywmm import WMMv2, date_utils
from src.models.wmm_model import WMMModel
from datetime import datetime, timedelta


class WMMCalculator:
    @staticmethod
    def calculate(model: WMMModel):
        decimal_year = date_utils.decimal_year(model.date)
        wmm = WMMv2()
        dec = wmm.get_declination(model.latitude, model.longitude, decimal_year, model.altitude)
        dip = wmm.get_dip_angle(model.latitude, model.longitude, decimal_year, model.altitude)
        ti = wmm.get_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bh = wmm.get_horizontal_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bx = wmm.get_north_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        by = wmm.get_east_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        bz = wmm.get_vertical_intensity(model.latitude, model.longitude, decimal_year, model.altitude)
        model.set_results(dec, dip, ti, bh, bx, by, bz)

    @staticmethod
    def calculate_next_year(model: WMMModel):
        current_date = datetime.strptime(model.date, '%Y-%m-%d')
        next_date = current_date + timedelta(days=365)  # This doesn't account for leap years
        next_year = next_date.strftime('%Y-%m-%d')
        next_model = WMMModel(latitude=model.latitude,
                              longitude=model.longitude,
                              altitude=model.altitude,
                              date=next_year)

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
            "bz": next_model.bz - model.bz,
        }
        return variation
