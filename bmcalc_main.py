from datetime import date, datetime, timedelta
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

        # ---- API call 1 ----
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
            print(f"\nYour Hebrew birthday is: {hebrew_date.get('displayEn')}")
        except Exception as e:
            print("There was a problem fetching the Hebrew date.")

        # ---- compute 13 years + 1 day ----
        bar_mitzvah_date = greg_date + relativedelta(years=13, days=1)
        print("You are bar mitzvah on:", bar_mitzvah_date.strftime("%Y-%m-%d"))
    
        # compute closest Shabbat on/after 13+1
        def next_shabbat(d):
            # Monday=0 ... Saturday=5, Sunday=6
            days_ahead = (5 - d.weekday()) % 7
            if days_ahead == 0:   # strictly after
                days_ahead = 7
            return d + timedelta(days=days_ahead)

        shabbat_date = next_shabbat(bar_mitzvah_date)

        # print("Shabbat date:", shabbat_date)
        # print("Weekday number:", shabbat_date.weekday())  # should be 5
        # if shabbat_date.weekday() == 5:
        #     print("✅ This is Saturday")
        # else:
        #     print("❌ This is not Saturday")

        # ---- API call 2 ----
        url = "https://www.hebcal.com/leyning"
        params = {
            "cfg": "json",
            "date": shabbat_date.strftime("%Y-%m-%d"),
            "i": "on",  # Israel readings; use "off" or omit for Diaspora
            }

        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("items", [])
        if not items:
            print("No leyning returned for that date.")
        else:
            shab_str = shabbat_date.strftime("%Y-%m-%d")
            item = next((it for it in items if it.get("date") == shab_str), items[0])
            name_en = (item.get("name") or {}).get("en")
            print("The Shabbat of your bar mitzvah is:", shab_str)
            print("Parsha:", name_en or "(unknown)")
            if name_he:
                print("Parsha (he):", name_he)

        input("\nPress Enter to return to the menu...")

    elif choice == "B":
        print("Enjoy your special parsha! Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")