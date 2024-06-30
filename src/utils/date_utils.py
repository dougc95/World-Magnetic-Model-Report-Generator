import calendar
from datetime import datetime, timedelta

class DateUtils:
    @staticmethod
    def decimal_year(date_str: str) -> float:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_year = datetime(date.year, 1, 1)
        end_of_year = datetime(date.year + 1, 1, 1)
        year_duration = (end_of_year - start_of_year).days
        year_elapsed = (date - start_of_year).days
        return date.year + year_elapsed / year_duration

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