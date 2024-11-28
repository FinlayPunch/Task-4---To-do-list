from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import sessionmaker
from setup_db import User, ToDo
from sqlalchemy import create_engine
import os
import sqlite3
import sqlalchemy

app = Flask(__name__)
app.secret_key = "secret_key"


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
    
    else:
        user_id = session['user_id']
        todos = db_session.query(ToDo).filter_by(user_id=user_id).all()

    return render_template('dashboard.html', user_id=session["user_id"], username=session["username"], todos = todos)

@app.route('/add_todo', methods=["POST"])
def add_todo():
    if "user_id" not in session:
        flash("Please log in to add a to-do.", "warning")
        return redirect(url_for('login'))
    
    task_description = request.form.get("task")
    user_id = session["user_id"]

    new_task = ToDo(task=task_description, user_id=user_id)
    db_session.add(new_task)
    db_session.commit()
    flash("To-Do added successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/delete_todo/<int:todo_id>', methods=["POST"])
def delete_todo(todo_id):

    if "user_id" not in session:
        flash("Please log in to delete a to-do.", "warning")
        return redirect(url_for('login'))

    task = db_session.query(ToDo).get(todo_id)

    if task and task.user_id == session["user_id"]:
        db_session.delete(task)
        db_session.commit()
        flash("To-Do deleted successfully!", "success")
    else:
        flash("To-Do not found or access denied.", "danger")
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)