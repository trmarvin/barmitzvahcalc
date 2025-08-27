from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from bmcalc_main import greg_date

# API 2 - PARSHA CALCULATOR

# This api uses the greg_date as input, so need to calculate age by adding 13 years and 1 day
# Example: if birthdate is 2010-05-15, calculate parsha for 2023-05-16

greg_date_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
bar_mitzvah_date = greg_date_obj + relativedelta(years=13, days=1)
print("Bar/Bat Mitzvah date:", bar_mitzvah_date.strftime("%Y-%m-%d"))

# response2 = requests.get("https://api.another-example.com/data2")
# parsha_calc = response2.json()