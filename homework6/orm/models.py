from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, CHAR, VARCHAR

Base = declarative_base()


class RequestsAmountModel(Base):
    __tablename__ = 'requests_amount'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Banner id={self.id}, name={self.data_name}, amount={self.amount}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_name = Column(CHAR(50), nullable=False)
    amount = Column(Integer, nullable=False)


class RequestsAmountByTypeModel(Base):
    __tablename__ = 'requests_amount_by_type'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Banner id={self.id}, data_name={self.data_name}, amount={self.amount}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_name = Column(CHAR(50), nullable=False)
    amount = Column(Integer, nullable=False)


class MostFrequentRequestsModel(Base):
    __tablename__ = 'most_frequent_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Banner id={self.id}, url={self.url}, amount={self.amount}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(50), nullable=False)
    amount = Column(Integer, nullable=False)


class HighestRequestWith4XXCodeModel(Base):
    __tablename__ = 'highest_request_with_4XX_code'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Banner id={self.id}, url={self.url}, exit_code={self.exit_code}, ' \
               f'size={self.size}, ip_address={self.ip_address}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(255), nullable=False)
    exit_code = Column(Integer, nullable=False)
    ip_address = Column(VARCHAR(50), nullable=False)
    size = Column(Integer, nullable=False)


class MostFrequentUsersWith5XXCodeModel(Base):
    __tablename__ = 'most_frequent_users_with_5XX_code'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Banner id={self.id}, ip_address={self.ip_address}, amount={self.amount}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(VARCHAR(50), nullable=False)
    amount = Column(Integer, nullable=False)
