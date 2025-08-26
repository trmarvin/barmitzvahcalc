from bmcalc_main import greg_date
import requests

# API 1
response1 = requests.get(f"https://www.hebcal.com/converter?cfg=json&gy={greg_date.year}&gm={greg_date.month}&gd={greg_date.day}&g2h=1")
hebrew_date = response1.json()