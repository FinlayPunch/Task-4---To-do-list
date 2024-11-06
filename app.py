from flask import Flask
import sqlalchemy
import sqlite3



conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT
    )
''')

cursor.execute("INSERT INTO users (name, age, email) VALUES ('Alice', 30, 'alice@example.com')")
cursor.execute("INSERT INTO users (name, age, email) VALUES ('Bob', 25, 'bob@example.com')")

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()



app = Flask(__name__)

@app.route('/')
def home():

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>My site</title>
        <link rel='stylesheet' type='text/css' href='/static/style.css'>
    </head>
    <body>
        <h1 class="main">Welcome</h1>
        <h2>Click on <a href="./table">table</a> or <a href="./images">image</a> to go to the associated page. Click <a href="https://www.wikipedia.org/">here</a> to go to wikipedia.</h2>
        <p id="homeP">On this website you can find a webpage with images, and a webpage with a table.</p>
    </body>
    </html>
    '''

    return html

app.run(debug=True, reloader_type='stat', port=5000)