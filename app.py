from flask import Flask, render_template
import sqlalchemy
import sqlite3


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

app.run(debug=True, reloader_type='stat', port=5000)