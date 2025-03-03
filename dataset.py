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

