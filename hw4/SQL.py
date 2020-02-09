#  изменен для HW 4
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pprint import pprint


engine = create_engine('sqlite:///parse-news.sqlite', echo=True)
Base = declarative_base()

class Lenta(Base):
    __tablename__='lenta'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    sourse      = Column(String(150))
    sourse_info = Column(String(250))
    name        = Column(String(250))
    url         = Column(String(250))
    date_time   = Column(String(50))
    date        = Column(String(50))

    def __init__(self,r):
        self.sourse = r[0]
        self.sourse_info = r[1]
        self.name = r[2]
        self.url = r[3]
        self.date_time = r[4]
        self.date = r[5]

class Yandex(Base):
    __tablename__='yandex'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    sourse      = Column(String(150))
    sourse_info = Column(String(250))
    name        = Column(String(250))
    url         = Column(String(250))
    date_time   = Column(String(50))
    date        = Column(String(50))

    def __init__(self, r):
        self.sourse = r[0]
        self.sourse_info = r[1]
        self.name = r[2]
        self.url = r[3]
        self.date_time = r[4]
        self.date = r[5]

class Mailru(Base):
    __tablename__='mail'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    sourse      = Column(String(150))
    sourse_info = Column(String(250))
    name        = Column(String(250))
    url         = Column(String(250))
    date_time   = Column(String(50))
    date        = Column(String(50))

    def __init__(self,r):
        self.sourse = r[0]
        self.sourse_info = r[1]
        self.name = r[2]
        self.url = r[3]
        self.date_time = r[4]
        self.date = r[5]

def openSession():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return(Session())

def addinSession(v, Obj):
    v.add(Obj)
    v.commit()

def closeSession(v):
    v.close()

if __name__ == "__main__":
    pass