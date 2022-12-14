from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, SMALLINT, DATETIME

Base = declarative_base()


class TestModel(Base):
    __tablename__ = 'test_users'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'id={self.id}, name={self.name}, surname={self.surname}, middle_name={self.middle_name}, ' \
               f'username={self.username}, password={self.password}, email={self.email}, access={self.access}, ' \
               f'active={self.active}, start_active_time={self.start_active_time}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    surname = Column(VARCHAR(255), nullable=False)
    middle_name = Column(VARCHAR(255), nullable=True)
    username = Column(VARCHAR(16), nullable=True, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False, unique=True)
    access = Column(SMALLINT, nullable=False)
    active = Column(SMALLINT, nullable=False)
    start_active_time = Column(DATETIME, nullable=True)
