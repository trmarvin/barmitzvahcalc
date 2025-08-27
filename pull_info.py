import requests
from bmcalc_main import parsha_israel, parsha_diaspora

# ---- API 3 ----

def get_parsha_text(parsha_israel, version="english"):
    # Step 1: Ask Sefaria when/where this parasha is next read
    url = f"https://www.sefaria.org/api/calendars/next-read/{parsha_israel}"
    nx = requests.get(url, timeout=10).json()

    ref = nx.get("ref")           # e.g., "Genesis 25:19-28:9"
    date_en = nx.get("date", {}).get("en")

    if not ref:
        print(f"No ref found for {parsha_name}")
        return None

    # Step 2: Fetch the Torah text for that ref
    text_url = f"https://www.sefaria.org/api/v3/texts/{ref}"
    text_resp = requests.get(text_url, params={"version": version}, timeout=10).json()

    verses = []
    if text_resp.get("versions"):
        verses = text_resp["versions"][0].get("text", [])

    return {
        "name": parsha_name,
        "ref": ref,
        "date": date_en,
        "verses": verses
    }

# Example usage:
israel_data = get_parsha_text(parsha_israel)
diaspora_data = get_parsha_text(parsha_diaspora)

print("Israel Parsha:", israel_data["name"], israel_data["ref"])
print("First 3 verses:", israel_data["verses"][:3])
print("\nDiaspora Parsha:", diaspora_data["name"], diaspora_data["ref"])
print("First 3 verses:", diaspora_data["verses"][:3])


