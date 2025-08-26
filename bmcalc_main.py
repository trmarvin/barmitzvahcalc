from datetime import datetime

# from date_convert import hebrew_date
# from parsha_find import parsha_calc
# from pull_info import parsha_info

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
            greg_birthdate = input("Please enter your birthdate on the civil (Gregorian) calendar in the format YYYY-MM-DD: ").strip()
            try:
                birthdate = datetime.strptime(greg_birthdate, "%Y-%m-%d").date()
                print("Valid date:", birthdate)
                break  # exit the loop if valid
            except ValueError:
                print("Invalid format. Please try again (use YYYY-MM-DD).")
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