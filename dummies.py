import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from passlib.apps import custom_app_context as pwd_context
 

""" Connecting MariaDB server"""
engine = create_engine(
    'mysql+pymysql://root@localhost/mydatabase?charset=utf8',
    connect_args = {
        'port': 3306
    },
    echo='debug',
    echo_pool=True
)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("hash1",pwd_context.encrypt("password"))
session.add(user)
 
user = User("hash2",pwd_context.encrypt("python"))
session.add(user)
 
user = User("hash3",pwd_context.encrypt("python"))
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()