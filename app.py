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

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
    # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
    # Check if the username already exists
        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            flash("Username already taken. Please choose another.", "danger")
            return redirect(url_for('signup'))
        # Hash the password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()
        
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to login first', 'warning')
        return redirect(url_for('login'))
    
    else:
        user_id = session['user_id']
        todos = db_session.query(ToDo).filter_by(user_id=user_id).order_by(ToDo.date.asc()).all()

    return render_template('dashboard.html', user_id=session["user_id"], username=session["username"], todos = todos)

@app.route('/addtask')
def add_task():
    if "user_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))
    return render_template('addtask.html')


@app.route('/submit_task', methods=["POST"])
def submit_task():
    if "user_id" not in session:
        flash("Please log in to add a task.", "warning")
        return redirect(url_for('login'))
    
    task_name = request.form.get("task")
    description = request.form.get("description")
    date = request.form.get("date")
    user_id = session["user_id"]
    category = request.form.get("category")

    new_task = ToDo(task=task_name, description=description, date=date, category=category, user_id=user_id)
    db_session.add(new_task)
    db_session.commit()
    flash("Task added successfully!", "success")
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

@app.route('/update_task/<int:todo_id>', methods=["GET"])
def update_task(todo_id):
    if "user_id" not in session:
        flash("Please log in to update a task.", "warning")
        return redirect(url_for('login'))
    
    task = db_session.query(ToDo).get(todo_id)
    if task and task.user_id == session["user_id"]:
        return render_template('update_task.html', task=task)
    else:
        flash("Task not found or access denied.", "danger")
        return redirect(url_for('dashboard'))


@app.route('/submit_update_task/<int:todo_id>', methods=["POST"])
def submit_update_task(todo_id):
    if "user_id" not in session:
        flash("Please log in to update a task.", "warning")
        return redirect(url_for('login'))
    
    task = db_session.query(ToDo).get(todo_id)
    if task and task.user_id == session["user_id"]:
        task.task = request.form.get("task")
        task.description = request.form.get("description")
        task.date = request.form.get("date")
        task.category = request.form.get("category")
        db_session.commit()
        flash("Task updated successfully!", "success")
    else:
        flash("Task not found or access denied.", "danger")
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)