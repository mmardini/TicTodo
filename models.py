from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    text = Column(String(50))
    order = Column(Integer, default=0)
    owner = Column(Integer, ForeignKey('users.id'))
    done = Column(Boolean, default=False)

    def __init__(self, text=None, order=None, owner=None):
        self.text = text
        self.order = order
        self.owner = owner

    def __repr__(self):
        return '<Task %r>' % (self.text)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(80), default="")

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)
