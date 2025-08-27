from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import requests

GREGORIAN_START = date(1582, 10, 15)

def welcome_menu():
    print("\nWelcome to the Bar/Bat Mitzvah Calculator!")
    print("This program will tell you the parsha (Shabbat Torah reading)")
    print("closest to your thirteenth Hebrew birthday, plus one day,")
    print("as required by Jewish law.")
    print("Please select an option:")
    print("A - Calculate Bar Mitzvah date")
    print("B - Exit")

hebrew_date = None
greg_date = None  # will be a datetime.date
bar_mitzvah_date = None

while True:
    welcome_menu()
    choice = input("Enter your choice: ").strip().upper()

    if choice == "A":
        # ---- input validation loop ----
        while True:
            birthdate = input("Please enter your birthdate (YYYY-MM-DD): ").strip()
            try:
                greg_date = datetime.strptime(birthdate, "%Y-%m-%d").date()
            except ValueError as e:
                print(f"Invalid date: {e}. Use YYYY-MM-DD.")
                continue
            if greg_date < GREGORIAN_START:
                print("Please use a date on/after 1582-10-15 (Gregorian reform).")
                continue
            if greg_date > date.today():
                print("Birthdate cannot be in the future.")
                continue
            break  # valid date

        # ---- API call ----
        url = "https://www.torahcalc.com/api/dateconverter/gregtoheb"
        params = {
            "year": greg_date.year,
            "month": greg_date.month,
            "day": greg_date.day,
            "afterSunset": "false",
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            hebrew_date = resp.json().get("data", {})
            print(f"\nYour Hebrew birthday is: {hebrew_date.get('displayEn')} "
                  f"\n{hebrew_date.get('displayGematriya')}")
        except Exception as e:
            print("There was a problem fetching the Hebrew date.")

        input("\nPress Enter to return to the menu...")

    # ---- compute 13 years + 1 day FIRST ----
        bar_mitzvah_date = greg_date + relativedelta(years=13, days=1)
        print("Your thirtheenth birthday:", bar_mitzvah_date.strftime("%Y-%m-%d"))
    
    elif choice == "B":
        print("Enjoy your special parsha! Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")