from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine(
    'mysql+pymysql://root@localhost/mydatabase?charset=utf8',
    connect_args = {
        'port': 3306
    },
    echo='debug',
    echo_pool=True
)
Base = declarative_base()
 
########################################################################
class User(Base):

    __tablename__= "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(350))

    def __init__(self, username, password):
        self.username = username
        self.password = password
 
# create tables
Base.metadata.create_all(engine)