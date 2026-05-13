import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE rides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    destination TEXT,
    seats INTEGER,
    time TEXT
)
''')

conn.close()

print("Database created successfully!")