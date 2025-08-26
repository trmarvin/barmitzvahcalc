import requests, psycopg2, json

# Connect to PostgreSQL
connection = psycopg2.connect(
    database="parsha",
    user="postgres",
    password="07Nathan30!",
    host="localhost",
    port="5432"
)  
cursor = connection.cursor()


greg_date = input("Enter a Gregorian date (YYYY-MM-DD): ")

# API 1 - HEBREW DATE CONVERTER
response1 = requests.get("/api/dateconverter/gregtoheb")
hebrew_date = response1.json()

# API 2 - PARSHA CALCULATOR
response2 = requests.get("https://api.another-example.com/data2")
parsha_calc = response2.json()

# API 3 - PARSHA INFO
response3 = requests.get("https://api.yet-another-example.com/data3")
parsha_info = response3.json()

# Process data from both APIs
print(hebrew_date)
print(parsha_calc)
print(parsha_info)
print("Please note, these results are only valid for birthdates after the time of the Gregorian calendar reform in 1582, and later in some locales.")

cursor.close()
connection.close()

def welcome_menu():
    print("Welcome to the Bar/Bat Mitzvah Calculator!")
    print("This program will tell you the parsha (Shabbat Torah reading) closest to your thirteenth Hebrew birthday, plus one day, as required by Jewish law.")
    print("Please select an option:")
    print("1. Calculate Bar Mitzvah date")
    print("2. Exit")
