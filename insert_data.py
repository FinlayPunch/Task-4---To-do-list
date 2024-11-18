from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash
from setup_db import User, ToDo

# Ensure you use `my_database.db`
engine = create_engine('sqlite:///my_database.db')  
Session = sessionmaker(bind=engine)
session = Session()

# Insert Users
user1 = User(username='john_doe', password=generate_password_hash('password123'))
user2 = User(username='jane_doe', password=generate_password_hash('mypassword'))

session.add(user1)
session.add(user2)
session.commit()

# Insert ToDo tasks
task1 = ToDo(task='Buy groceries', done=False, user_id=user1.id)
task2 = ToDo(task='Clean the house', done=False, user_id=user2.id)

session.add(task1)
session.add(task2)
session.commit()

print("Data inserted")