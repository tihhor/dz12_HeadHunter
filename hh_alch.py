import pprint

from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from datetime import datetime

engine = create_engine('sqlite:///hh_orm.sqlite', echo=False)
Base = declarative_base()

class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    search_str = Column(String)
    vacans = Column(Integer)
    aver_sal = Column(Numeric)
    skills = relationship('Skills', back_populates='request')

    def __str__(self):
        return f'{self.id}: {self.date} найдено {self.vacans}'

    def __init__(self, search_str, vacans, aver_sal):
        now = datetime.now()
        self.date = now
        self.search_str = search_str
        self.vacans = vacans
        self.aver_sal = aver_sal


class Skills(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    skills_name = Column(String)
    skills_qnt = Column(Integer)
    skill_id = Column(Integer, ForeignKey('request.id'))
    request = relationship('Request', back_populates='skills')

    def __str__(self):
        return f'{self.skills_name} {self.skills_qnt}'

    def __init__(self, id, skills_name, skills_qnt, skill_id):
        # self.id = id
        self.skills_name = skills_name
        self.skills_qnt = skills_qnt
        self.skill_id = skill_id

def save_data_orm(data):

    # Создание таблицы
    Base.metadata.create_all(engine)
    # Заполняем таблицы
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()

    now = datetime.now()

    # сохраняем текст запроса

    session.add(Request(data['request_text'], data['vacancies_total'], data['average_salary']))
    # находим максиимальный номер записи
    requests = session.query(Request).all()
    next_id = len(requests)

    #добавляем записи в таблицу вакансий с ключом последнего запроса
    for item in data['key_skills']:
        session.add(Skills(next_id, item[0], item[1], next_id))

    session.commit()

    # печатаем историю запросов и найденные три ключевые вакансии
    reqs = session.query(Request).all()

    for req in reqs:
        print(req)
        sks = session.query(Skills).filter(Skills.skill_id == req.id).all()
        for sk in sks:
            print('  ', sk)


