from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from urllib.parse import quote
import requests
import psycopg2
import re

GREGORIAN_START = date(1582, 10, 15)

def welcome_menu():
    print("\nWelcome to the Bar/Bat Mitzvah Calculator!")
    print("This program will tell you the parsha (Shabbat Torah reading).")
    print("closest to your thirteenth Hebrew birthday ( plus one day).")
    print("Please select an option:")
    print("A - Calculate Bar Mitzvah date")
    print("B - Exit")

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

        # ---- API call 1: convert from gregorian to hebrew date ----
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

        # ---- determine gender to calculate Bar/Bat Mitzvah date ----
        while True:
            print("Please select an option:")
            print("F - I am female")
            print("M - I am male")

            choice = input("Enter your choice: ").strip().upper()

            if choice == "F":
                # ---- compute 12 years + 1 day ----
                bar_mitzvah_date = greg_date + relativedelta(years=12, days=1)
                print("You are bat mitzvah on:", bar_mitzvah_date.strftime("%Y-%m-%d"))
                break  # exit the loop
            elif choice == "M":
                # ---- compute 13 years + 1 day ----
                bar_mitzvah_date = greg_date + relativedelta(years=13, days=1)
                print("You are bar mitzvah on:", bar_mitzvah_date.strftime("%Y-%m-%d"))
                break  # exit the loop
            else:
                print("Invalid choice. Please try again.\n")

        # ---- compute closest Shabbat on/after 12+1 or 13+1 ----
        def next_shabbat(d):
            # Monday=0 ... Saturday=5, Sunday=6
            days_ahead = (5 - d.weekday()) % 7
            if days_ahead == 0:   
                days_ahead = 7
            return d + timedelta(days=days_ahead)

        shabbat_date = next_shabbat(bar_mitzvah_date)

        # ---- API call set 2: find parsha for bar/bat mitzvah date ----
        def get_parsha_name(shabbat_date, israel: bool) -> str | None:
            url = "https://www.hebcal.com/leyning"
            params = {
                "cfg": "json",
                "date": shabbat_date.strftime("%Y-%m-%d"),
                }
            params["i"] = "on" if israel else "off"

            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items", [])
            if not items:
                return None

            shab_str = shabbat_date.strftime("%Y-%m-%d")
            item = next((it for it in items if it.get("date") == shab_str), items[0])
            return (item.get("name") or {}).get("en")

        shab_str = shabbat_date.strftime("%Y-%m-%d")
        
        try:
            parsha_israel   = get_parsha_name(shabbat_date, israel=True)
            parsha_diaspora = get_parsha_name(shabbat_date, israel=False)

            print("The Shabbat of your bar mitzvah is:", shab_str)

            # Normalize for comparison
            if parsha_israel and parsha_diaspora:
                if parsha_israel.strip().lower() == parsha_diaspora.strip().lower():
                    # Same parsha → only print once
                    print("Parsha (Israel & Diaspora):", parsha_israel)
                else:
                    # Different → print both
                    print("Parsha (Israel):  ", parsha_israel)
                    print("Parsha (Diaspora):", parsha_diaspora)
            else:
                # If one or both are missing
                print("Parsha (Israel):  ", parsha_israel or "(unknown)")
                print("Parsha (Diaspora):", parsha_diaspora or "(unknown)")

        except requests.RequestException as e:
            print("Problem fetching parsha data:", e)

        name_israel   = parsha_israel.strip().lower()
        name_diaspora = parsha_diaspora.strip().lower()
        
        # ---- API 3: get next read time info from Sefaria ----
        def next_parsha_info(parsha_name: str):
            url = f"https://www.sefaria.org/api/calendars/next-read/{parsha_name.strip()}"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            nx = r.json()
            
            ref = (nx.get("parasha") or {}).get("ref")
            date_str = nx.get("date")  # e.g. "2026-06-20T00:00:00"
            he_date = (nx.get("he_date") or {}).get("en")
    
            # parse Gregorian date string
            date_en = None
            if date_str:
                date_en = datetime.fromisoformat(date_str.replace("Z","")).strftime("%A, %B %d, %Y")
    
            return {
                "name": parsha_name,
                "ref": ref,
                "greg_date": date_en,
                "heb_date": he_date
            }

        # ---- print next time parsha will be read ----
        info_israel   = next_parsha_info(parsha_israel)
        info_diaspora = next_parsha_info(parsha_diaspora)

        if name_israel == name_diaspora:
            # Same parsha → only print once
            print(f"Both Israel and Diaspora will next read {parsha_israel} on {info_israel['greg_date']} / {info_israel['heb_date']}.")
        else:
            # Different → print both separately
            print(f"Israel next reads {parsha_israel} on {info_israel['greg_date']} / {info_israel['heb_date']}.")
            print(f"Diaspora reads: {parsha_diaspora} on {info_diaspora['greg_date']} / {info_diaspora['heb_date']}.")

        def get_conn():
            return psycopg2.connect(
                dbname="parsha",
                user="postgres",       
                password="07Nathan30!",   
                host="localhost",
                port="5432"
            )
        # ---- DB: fetch parsha summary ----
        def fetch_parsha_row(conn, name: str):
            sql = """
                SELECT name_eng, book_eng, summary
                FROM public.parsha_summaries
                WHERE name_eng ILIKE %s
                LIMIT 1;
            """
            with conn.cursor() as cur:
                cur.execute(sql, (name,))
                row = cur.fetchone()
                if row:
                    name_eng, book_eng, summary = row
                    return {"name_eng": name_eng, "book_eng": book_eng, "summary": summary}
            return None

        def fetch_parsha_flexible(conn, raw_name: str):
            name = raw_name.strip()
            hit = fetch_parsha_row(conn, name)
            if hit:
                return [hit]

            # Try splitting on hyphen/dash (for doubled parshas)
            parts = re.split(r"[-–—]", name)
            results = []
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                row = fetch_parsha_row(conn, part)
                if row:
                    results.append(row)
            return results

        def show_parsha_info(parsha_israel: str, parsha_diaspora: str):
            same = parsha_israel.strip().lower() == parsha_diaspora.strip().lower()

            with get_conn() as conn:
                names = [parsha_israel] if same else [parsha_israel, parsha_diaspora]

                for nm in names:
                    rows = fetch_parsha_flexible(conn, nm)
                    if not rows:
                        print(f"\nNo match found for '{nm}'.")
                        continue

                    label = "Israel & Diaspora" if same else ("Israel" if nm == parsha_israel else "Diaspora")
                    # print(f"\n{label}: {nm}")
                    for r in rows:
                        print(f"• {r['name_eng']} summary — from Sefer {r['book_eng']}")
                        print(r["summary"])

        show_parsha_info(parsha_israel, parsha_diaspora)
        
        input("\nPress Enter to return to the menu...")

    elif choice == "B":
        print("Enjoy your special parsha! Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")