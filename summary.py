import psycopg2
import re
from bmcalc_main import parsha_israel, parsha_diaspora

def get_conn():
    """Connect to your Postgres database 'parsha'."""
    return psycopg2.connect(
        dbname="parsha",
        user="postgres",       
        password="07Nathan20!",   
        host="localhost",
        port="5432"
    )

def fetch_parsha_row(conn, name: str):
    """Look up a parsha by name (case-insensitive)."""
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
    """
    First try the full name. If not found and it looks like a combined parsha
    (e.g. 'Matot-Masei'), split and look up each half separately.
    """
    name = raw_name.strip()
    hit = fetch_parsha_row(conn, name)
    if hit:
        return [hit]

    # Try splitting on hyphen/dash
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
            print(f"\n{label}: {nm}")
            for r in rows:
                print(f"• {r['name_eng']} — {r['book_eng']}")
                print(r["summary"])

# Example usage:
parsha_israel = "Bereshit"
parsha_diaspora = "Bereshit"
print(show_parsha_info(parsha_israel, parsha_diaspora))