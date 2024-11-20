from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import sessionmaker
from setup_db import User, ToDo
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = "sercet_key"


engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db_session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully', 'info')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username or password', 'danger')

    return render_template('login.html')

@app.route('/signup')
def signup():
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to login first', 'warning')
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_id=session["user_id"], username=session["username"])


if __name__ == '__main__':
    app.run(debug=True, port=5000)