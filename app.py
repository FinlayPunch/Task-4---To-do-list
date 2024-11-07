from flask import Flask, render_template
import sqlite3
import sqlalchemy

app = Flask(__name__)

@app.route('login')
def home():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)