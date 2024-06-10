import calendar
from datetime import datetime

class DateUtils:
    @staticmethod
    def decimal_year(year: str) -> float:
        date_object = datetime.strptime(year, '%Y-%m-%d').date()
        days_in_year = 366 if calendar.isleap(date_object.year) else 365
        return date_object.year + (date_object.timetuple().tm_yday / days_in_year)