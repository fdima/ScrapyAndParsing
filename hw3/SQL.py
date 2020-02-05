from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///parse.sqlite', echo=True)
Base = declarative_base()

class Hh(Base):
    __tablename__='hh'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    site = Column(String(150)) #site
    name = Column(String(255)) #наименование вакансии
    sm1 = Column(Integer) # оплата от
    sm2 = Column(Integer) # оплата до
    url = Column(String(255)) # url вакансии на сайте

    def __init__(self,site, name, sm1, sm2, url):
        self.site = site
        self.name = name
        self.sm1 = sm1
        self.sm2 = sm2
        self.url = url

class SuperJ(Base):
    __tablename__='SuperJ'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    site = Column(String(150)) #site
    name = Column(String(255)) #наименование вакансии
    sm1 = Column(Integer) # оплата от
    sm2 = Column(Integer) # оплата до
    url = Column(String(255)) # url вакансии на сайте
    company = Column(String(255))
    companyUrl = Column(String(255))

    def __init__(self,site, name, sm1, sm2, url,company,companyUrl):
        self.site = site
        self.name = name
        self.sm1 = sm1
        self.sm2 = sm2
        self.url = url
        self.company = company
        self.companyUrl = companyUrl

def openSession():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return(Session())

def addinSession(v, Obj):
# vac = Hh('hh.ru','vac1', 10000 , 30000, 'urlsdsd1')
    # v.add(Hh('hh.ru','vac1', 10000 , 30000, 'urlsdsd1111'))
    v.add(Obj)
    v.commit()
# session.add_all([User("kolia", "Cool Kolian[S.A.]","kolia$$$", 28),
#                    User("zina", "Zina Korzina", "zk18", 54)])
# for instance in session.query(User).filter(User.age > 30):
    # print(instance.name, instance.password)
# session.commit()

def closeSession(v):
    v.close()


if __name__ == "__main__":
    # session = openSession()
    # addinSession(session, Hh('hh.ru','vac1', 10000 , 30000, 'urlsdsd1'))
    # closeSession(session)
    print('!')
