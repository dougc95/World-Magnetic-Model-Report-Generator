import calendar
from datetime import datetime, timedelta

class DateUtils:
    @staticmethod
    def date_range(start_date: str, end_date: str, step_days: int):
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        if step_days <= 0:
            raise ValueError("step_days must be a positive integer")

        step = timedelta(days=step_days)
        dates = []
        current_date = start
        while current_date <= end:
            dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += step
        return dates
    
    @staticmethod
    def decimal_year(date_str: str) -> float:
        try:
            date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        days_in_year = 366 if calendar.isleap(date_object.year) else 365
        return date_object.year + (date_object.timetuple().tm_yday / days_in_year)


if __name__ == "__main__":
    try:
        print(DateUtils.date_range("2024-01-01", "2024-01-10", 2))
        print(DateUtils.decimal_year("2024-07-01"))
    except ValueError as e:
        print(e)
