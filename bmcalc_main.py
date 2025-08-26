from date_convert import hebrew_date
from parsha_find import parsha_calc
from pull_info import parsha_info

def welcome_menu():
    print("Welcome to the Bar/Bat Mitzvah Calculator!")
    print("This program will tell you the parsha (Shabbat Torah reading) closest to your thirteenth Hebrew birthday, plus one day, as required by Jewish law.")
    print("Please select an option:")
    print("1. Calculate Bar Mitzvah date")
    print("2. Exit")

# Process data from all APIs
print(hebrew_date)
print(parsha_calc)
print(parsha_info)
print("Please note, these results are only valid for birthdates after the time of the Gregorian calendar reform in 1582, and later in some locales.")
