from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Define the Base
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    todos = relationship('ToDo', back_populates='user')

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Define the ToDo model
class ToDo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='todos')

# Database setup
engine = create_engine('sqlite:///my_database.db')  # Ensure consistent database
Base.metadata.create_all(engine)  # Create tables if they don't exist
print("Database and tables created")
