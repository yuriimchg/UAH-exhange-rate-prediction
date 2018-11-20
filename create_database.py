from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime


#TODO: Create database with tables. Every table will be exported later as csv
Base = declarative_base()

class Exchange(Base):
    """ Create table for exchange rates
    https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date=20181120&json
    """
    __tablename__ = 'exchange'
    id = Column(Integer, primary_key=True)
    exchangedate = Column(DateTime, default=datetime.utcnow)
    r030 = Column(Integer)
    txt = Column(String)
    rate = Column(Float)
    сс = Column(String(3))

    def __repr__(self):
        return f'<Exchange(r030={self.r030}, txt={self.txt}, ' \
               f'rate={self.rate}, cc={self.cc}, exchangedate={self.sexchangedate})>'


class Monetary(Base):
    """  https://bank.gov.ua/NBUStatService/v1/statdirectory/monetary?sort=ind&order=asc&k076=Total&date=20030201&json"""
    __tablename__ = 'monetary'
    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='M')
    m0_cash = Column(Float)     # id_api = M0  == cash outside of deposits
    m1_aggregate = Column(Float)  # id_api = M1 == M0 + deposits in UAH
    m2_aggregate = Column(Float)  # id_api = M2 == M1 + deposits in $
    m3_aggregate = Column(Float)  # id_api = M3 == M2 + securities

    def __repr__(self):
        return f'<Monetary(dt={self.dt}, freq={self.freq}, m0_cash={self.m0_cash}, ' \
               f'm1_aggregate={self.m1_aggregate}, m2_aggregate={self.m2_aggregate}, m3_aggregate={self.m3_aggregate})>'


class BanksIncomesExpenses(Base):
    """https://bank.gov.ua/NBUStatService/v1/statdirectory/banksincexp?date=20090201&period=m&json"""
    tablename = 'banksincexp'
    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='M')
    total_income = Column(Float) # id_api = BS2_IncomeTotal
    total_expense = Column(Float) # id_api = BS2_ExpensesTotal
    income_tax = Column(Float) # id_api = BS2_ExpTaxIncome
    net_profit = Column(Float) # id_api = BS2_NetProfitLoss

    def __repr__(self):
        return f'<BanksIncExp(dt={self.dt}, freq={self.freq}, total_income={self.total_income}, total_expense=' \
               f'{self.total_expense}, income_tax={self.income_tax}, net_profit={self.net_profit})>'


class Investment(Base):
    """https://bank.gov.ua/NBUStatService/v1/statdirectory/interinvestpos?date=200301&s181=Total&json"""
    __tablename__ = 'interinvest'
    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='Q')
    assets = Column(Float) # id_api = IIP_A, s181 = Total
    net_inv_pos = Column(Float) # id_api = IIP_Net, s181 = Total
    direct_inv = Column(Float) # id_api = FDI_A, s181 = Total

    def __repr__(self):
        return f'<InterInvest(dt={self.dt}, freq={self.freq}, assets={self.assets},' \
               f' net_inv_pos={self.net_inv_pos}, direct_inv={self.direct_inv})>'











