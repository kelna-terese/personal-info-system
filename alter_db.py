# alter_db.py
import sqlite3
from pathlib import Path

# Resolve DB path (works when run normally)
DB_PATH = Path(__file__).parent / "PIS.db"

# If you prefer editor-friendly (no _file_ warning), use:
# DB_PATH = Path("PIS.db")

columns_to_add = {
    "blood_group": "TEXT",
    "height": "REAL",
    "weight": "REAL",
    "allergies": "TEXT",
    "emergency_name": "TEXT",
    "emergency_phone": "TEXT"
}

def get_existing_columns(conn, table_name="persons"):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    rows = cur.fetchall()
    # PRAGMA table_info returns rows where name is column name (index 1)
    return {r[1] for r in rows}

def main():
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found. Make sure you're in the project folder.")
        return

    conn = sqlite3.connect(DB_PATH)
    existing = get_existing_columns(conn, "persons")
    cur = conn.cursor()

    for col, col_type in columns_to_add.items():
        if col in existing:
            print(f"⚠  Column '{col}' already exists — skipping.")
            continue
        sql = f"ALTER TABLE persons ADD COLUMN {col} {col_type};"
        print(f"Adding column: {col} {col_type}")
        cur.execute(sql)

    conn.commit()
    conn.close()
    print("🎉 Done — table updated.")
    # Print final column list
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(persons)")
    for r in cur.fetchall():
        print(f" - {r[1]} ({r[2]})")
    conn.close()

if __name__== "__main__":
    main()