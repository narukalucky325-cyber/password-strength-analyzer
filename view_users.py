import sqlite3

# CONNECT DATABASE
conn = sqlite3.connect("password_history.db")

cursor = conn.cursor()

# SHOW ALL TABLES
cursor.execute("""
SELECT name FROM sqlite_master
WHERE type='table';
""")
tables = cursor.fetchall()

print("\nDATABASE TABLES:\n")

for table in tables:
    print(table)

# SHOW USERS TABLE DATA
print("\nUSERS TABLE DATA:\n")

cursor.execute("SELECT * FROM users")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()