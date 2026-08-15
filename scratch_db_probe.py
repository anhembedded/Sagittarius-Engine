import sqlite3
from pathlib import Path
root = Path(r'c:\Users\hoang\Documents\Sagittarius-Engine\Sagittarius_Elite_Warrior\database')
for db in root.glob('*.db'):
    con = sqlite3.connect(db)
    cur = con.cursor()
    print('DB', db.name)
    try:
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        print('TABLES', tables)
        for table in tables:
            try:
                count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                print('COUNT', table, count)
            except Exception as exc:
                print('COUNT_ERR', table, repr(exc))
    finally:
        con.close()
