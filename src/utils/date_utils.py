import calendar
from datetime import datetime, timedelta

class DateUtils:
    @staticmethod
    def date_range(start_date: str, end_date: str, step_days: int):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        step = timedelta(days=step_days)
        dates = []
        current_date = start
        while current_date <= end:
            dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += step
        return dates
    
    @staticmethod
    def decimal_year(date_str: str) -> float:
        date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
        days_in_year = 366 if calendar.isleap(date_object.year) else 365
        return date_object.year + (date_object.timetuple().tm_yday / days_in_year)