import sqlite3
import os
import shutil

db_path = r'C:\Users\HAI\.agent-browser\profiles\ai_profile\Default\Network\Cookies'
temp_db = r'C:\Users\HAI\.agent-browser\profiles\ai_profile\Default\Network\Cookies_temp'

if os.path.exists(db_path):
    shutil.copy2(db_path, temp_db)
    conn = sqlite3.connect(temp_db)
    cur = conn.cursor()
    cur.execute("SELECT host_key, name FROM cookies WHERE host_key LIKE '%tiktok%'")
    rows = cur.fetchall()
    print(f"Total TikTok cookies: {len(rows)}")
    for r in rows:
        print(f"  Cookie: {r[1]} ({r[0]})")
    conn.close()
    try:
        os.remove(temp_db)
    except Exception:
        pass
else:
    print("Cookies DB not found")
