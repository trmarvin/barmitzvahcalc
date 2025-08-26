from datetime import datetime, date

# from date_convert import hebrew_date
# from parsha_find import parsha_calc
# from pull_info import parsha_info

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
        while True:
            s = input("Please enter your birthdate (YYYY-MM-DD): ").strip()
            try:
                birthdate = datetime.strptime(s, "%Y-%m-%d").date()
            except ValueError as e:
                print(f"Invalid date: {e}. Use YYYY-MM-DD.")
                continue

            if birthdate < GREGORIAN_START:
                print("Please use a date on/after 1582-10-15 (Gregorian reform).")
                continue
            if birthdate > date.today():
                print("Birthdate cannot be in the future.")
                continue

            print("Valid date:", birthdate)
            break  

    elif choice == "B":
        print("Enjoy your special parsha! Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")


# Display the results
# print(hebrew_date)
# print(parsha_calc)
# print(parsha_info)
print("Please note, these results are only valid for birthdates after the time of the Gregorian calendar reform in 1582, and later in some locales.")