import sqlite3

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT
    )
''')

# Insert data
cursor.execute("INSERT INTO users (name, age, email) VALUES ('Alice', 30, 'alice@example.com')")
cursor.execute("INSERT INTO users (name, age, email) VALUES ('Bob', 25, 'bob@example.com')")

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Print data
for row in rows:
    print(row)

# Commit and close
conn.commit()
conn.close()