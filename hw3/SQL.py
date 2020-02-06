from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pprint import pprint


engine = create_engine('sqlite:///parse.sqlite', echo=True)
Base = declarative_base()

class Hh(Base):
    __tablename__='hh'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    site = Column(String(150)) #site
    name = Column(String(255)) #наименование вакансии
    sm1 = Column(Integer) # оплата от
    sm2 = Column(Integer) # оплата до
    url = Column(String(255)) # url вакансия на сайте

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
    url = Column(String(255)) # url вакансия на сайте
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
    if (findUrl(Obj.__class__, Obj.url) == 0):
        v.add(Obj)
        v.commit()
# session.add_all([User("kolia", "Cool Kolian[S.A.]","kolia$$$", 28),
#                    User("zina", "Zina Korzina", "zk18", 54)])
# for instance in session.query(User).filter(User.age > 30):
    # print(instance.name, instance.password)
# session.commit()

def closeSession(v):
    v.close()


def findSalary(obj, smin):
    a = []
    s = openSession()
    rows = s.query(obj).filter(obj.sm1 > smin)
    # s.commit()
    closeSession(s)
    for row in rows:
        a.append ([row.url,row.sm1,row.sm2])
    return (a)

def findUrl(obj, urls):
    s = openSession()
    count = s.query(obj.url).filter(obj.url == urls).count()
    closeSession(s)
    return(count)

if __name__ == "__main__":
    # session = openSession()
    # addinSession(session, Hh('hh.ru','vac1', 10000 , 30000, 'urlsdsd1'))
    # closeSession(session)
    # 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД
    # 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
    # 3*)Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта
    i = 40000 
    print (f"Размер минимальной оплаты больше: {i}")
    pprint(findSalary(Hh,i))
    pprint(findSalary(SuperJ,i))
    print("---")
    pprint(findUrl(SuperJ, 'https://www.superjob.ru/vakansii/administrator-salona-krasoty-26378393.html'))
