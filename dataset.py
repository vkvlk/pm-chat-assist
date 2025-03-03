# Data loader , processer and utils

import pandas as pd
import holidays
from datetime import datetime, timedelta
from typing import List, Tuple
from config import settings

class DateUtils:
    """Utility class for handling date-related operations"""
    
    def __init__(self):
        """Initialize with US holidays"""
       # self.us_holidays = holidays.US()
        self.us_holidays = holidays.country_holidays(country=settings.country_code,years=settings.default_years)
    
    def is_holiday(self, date: datetime) -> bool:
        """Check if a given date is a holiday"""
        return date in self.us_holidays
    
    def is_weekend(self, date: datetime) -> bool:
        """Check if a given date is a weekend"""
        return date.weekday() >= 5  # 5 = Saturday, 6 = Sunday 
    
    def get_next_business_day(self, date: datetime) -> datetime:
        """Get the next business day after a given date"""
        next_day = date + timedelta(days=1)
        while self.is_holiday(next_day) or self.is_weekend(next_day):
            next_day += timedelta(days=1)
        return next_day
    
    def calculate_business_days(self, start_date: datetime, end_date: datetime) -> int:
        """Calculate number of business days between two dates"""
        business_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            if not (self.is_holiday(current_date) or self.is_weekend(current_date)):
                business_days += 1
            current_date += timedelta(days=1)
            
        return business_days
    
    def get_holiday_name(self, date: datetime) -> str:
        """Get the name of the holiday for a given date"""
        return self.us_holidays.get(date, '')
    
    def find_impacted_dates(self, start_date: datetime, end_date: datetime) -> List[Tuple[datetime, str]]:
        """Find all holidays and weekends between two dates"""
        impacted_dates = []
        current_date = start_date
        
        while current_date <= end_date:
            if self.is_holiday(current_date):
                impacted_dates.append((current_date, f"Holiday: {self.get_holiday_name(current_date)}"))
            elif self.is_weekend(current_date):
                impacted_dates.append((current_date, "Weekend"))
            current_date += timedelta(days=1)
            
        return impacted_dates
    
    def get_holidays_list_by_range(self, start_year: int, end_year: int) -> str:
        """Generate a list of US federal holidays for the specified years"""
        holiday_list = []
        for year in range(start_year, end_year + 1):
            # Get the holiday dict for the specific year
            year_holidays = holidays.US(years=year)
            # Extract only the date:name pairs and sort by date
            holiday_pairs = {date: name for date, name in year_holidays.items()}
            sorted_holidays = sorted(holiday_pairs.items())
            
            # Format the holidays for the year
            year_holidays_formatted = []
            for date, name in sorted_holidays:
                year_holidays_formatted.append(f"{date.strftime('%Y-%m-%d')}: {name}")
            
            holiday_list.append(f"US Federal Holidays {year}:\n" + "\n".join(year_holidays_formatted))
        
        return "\n\n".join(holiday_list)
    

def load_and_format_data() -> str:
    dt = DateUtils()
    # Load project schedule data
    df = pd.read_excel(settings.data_file_path)

    # Add metadata header
    data_context = f"""
    ## Project Schedule Data Context
    - Date Format: YYYY-MM-DD
    - Current Date: {datetime.today().strftime('%Y-%m-%d')}
    - Federal Holidays: {dt.get_holidays_list_by_range(settings.default_years[0], settings.default_years[-1])}
    - Weekend Definition: Saturday/Sunday
    - Task Relationships: FS=Finish-to-Start, SS=Start-to-Start, 4FS+43= Task 4 Finish-to-Start with offset +43 days
    """

    # Convert to LLM-friendly format
    formatted_data = data_context + "\n\n## Task List\n" + df.to_markdown()
    return formatted_data

