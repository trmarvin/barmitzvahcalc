from datetime import datetime, date
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

while True:
    welcome_menu()
    choice = input("Enter your choice: ").strip().upper()

    if choice == "A":
        # --- input validation loop ---
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

            print("Valid date:", greg_date)
            break

        url = "https://www.torahcalc.com/api/dateconverter/gregtoheb"
        params = {
            "year": greg_date.year,
            "month": greg_date.month,
            "day": greg_date.day,
            "afterSunset": "false",
        }

        hebrew_date = {
            'success': True,
            'data': {
            'year': 5738,
            'month': 3,
            'day': 18,
            'monthName': 'Sivan',
            'displayEn': '18th of Sivan, 5738',
            'displayHe': '18 סִיוָן, 5738',
            'displayGematriya': 'י״ח סִיוָן תשל״ח'
            }
        }

        data = hebrew_date["data"]

        print("Your Hebrew birthday is:", data["displayEn"])
        print("Hebrew:", data["displayGematriya"])

    elif choice == "B":
        print("Enjoy your special parsha! Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
