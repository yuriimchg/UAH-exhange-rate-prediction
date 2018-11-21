from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime

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
    cc = Column(String(3))

    def __repr__(self):
        return f'<Exchange(r030={self.r030}, txt={self.txt}, ' \
               f'rate={self.rate}, cc={self.cc}, exchangedate={self.sexchangedate})>'


class Monetary(Base):
    """ https://bank.gov.ua/NBUStatService/v1/statdirectory/monetary?sort=ind&order=asc&k076=Total&date=20030201&json"""
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
    total_income = Column(Float)  # id_api = BS2_IncomeTotal
    total_expense = Column(Float)  # id_api = BS2_ExpensesTotal
    income_tax = Column(Float)  # id_api = BS2_ExpTaxIncome
    net_profit = Column(Float)  # id_api = BS2_NetProfitLoss

    def __repr__(self):
        return f'<BanksIncExp(dt={self.dt}, freq={self.freq}, total_income={self.total_income}, total_expense=' \
               f'{self.total_expense}, income_tax={self.income_tax}, net_profit={self.net_profit})>'


class Investment(Base):
    """https://bank.gov.ua/NBUStatService/v1/statdirectory/interinvestpos?date=200301&s181=Total&json"""
    __tablename__ = 'interinvest'
    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='Q')
    assets = Column(Float)  # id_api = IIP_A, s181 = Total
    net_inv_pos = Column(Float)  # id_api = IIP_Net, s181 = Total
    direct_inv = Column(Float)  # id_api = FDI_A, s181 = Total

    def __repr__(self):
        return f'<InterInvest(dt={self.dt}, freq={self.freq}, assets={self.assets},' \
               f' net_inv_pos={self.net_inv_pos}, direct_inv={self.direct_inv})>'


class GrossExtDebt(Base):
    """https://bank.gov.ua/NBUStatService/v1/statdirectory/grossextdebt?date=200401&id_api=ed&json"""
    __tablename__ = 'grossextdebt'
    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='Q')
    grossextdebt = Column(Float)  # id_api=ED

    def __repr__(self):
        return f'<GrossExtDebt(dt={self.dt}, freq={self.freq}, grossextdebt={self.grossextdebt})>'


class Inflation(Base):
    """"""
    __tablename__ = 'inflation'
    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='M')
    ku = Column(String(5))
    tzep = Column(String(5))
    price_cpi = Column(Float)  # id_api = prices_price_cpi, mcrd081=Total -- Consumer price index
    price_ci = Column(Float)    # id_api = prices_price_ci, mcrd081=Total -- Core inflation

    def __repr__(self):
        return f'<Inflation(dt={self.dt}, freq={self.freq}, ku={self.ku}, tzep={self.tzep}' \
               f'price_cpi={self.price_cpi}, price_ci={self.price_ci})>'


class EconomicActivity(Base):
    """https://bank.gov.ua/NBUStatService/v1/statdirectory/economicactivity?period=m&id_api=ea_trade_rte&date=201504&json"""
    __tablename__ = 'economicactivity'
    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='Q')
    gross_dom_prod = Column(Float)
    gross_surplus = Column(Float)
    employee_compensation = Column(Float)  # id_api = ea_gdp_is_emp_comp & tzep = F_& mcr210i": "TOTAL" & "mcrk110": "Total" & tzep=F_
    gross_val_added = Column(Float)  # id_api = ea_gdp_ps_gv_add & tzep = F_& "mcr210i": "TOTAL" & "mcrk110": "Total" & tzep=F_
    gross_surplus_mixed_inc = Column(Float)  #  id_api = ea_gdp_is_gross_surplus & tzep = F_& "mcr210i": "TOTAL" & "mcrk110": "Total" & tzep=F_
    gross_fixed_cap_form = Column(Float)  #  id_api = ea_gdp_es_gfcf & tzep = F_& "mcr210i": "TOTAL" & "mcrk110": "Total" & tzep=F_
    net_export = Column(Float) #id_api = ea_gdp_es_net_exp & tzep = F_ & "mcr210i": "TOTAL" & "mcrk110": "Total" & tzep=F_
    exports = Column(Float)  # id_api = ea_gdp_es_net_egs  & "mcr210i": "TOTAL" & "mcrk110": "Total" & tzep=F_
    imports = Column(Float)  # id_api = ea_gdp_es_igs  & "mcr210i": "TOTAL" & "mcrk110": "Total" & tzep=F_
    gross_cap_form = Column(Float)  # id_api = ea_gdp_es_gf &  & "mcr210i": "TOTAL" & "mcrk110": "Total" & tzep=F_

    def __repr__(self):
        return f'<EconomicActivity(dt={self.dt}, freq={self.freq}, gross_dom_prod={self.gross_dom_prod},' \
               f' gross_surplus={self.gross_surplus}, employee_compensation={self. employee_compensation}, ' \
               f'gross_val_added={self.gross_val_added}, gross_surplus_mixed_inc={self.gross_surplus_mixed_inc}, ' \
               f'gross_fixed_cap_form={self.gross_fixed_cap_form}, net_export={self.net_export}, ' \
               f'exports={self.exports}, imports={self.imports}, exports={self.exports},' \
               f'gross_cap_form={self.gross_cap_form})>'


class Budget(Base):
    """https://bank.gov.ua/NBUStatService/v1/statdirectory/budget?period=m&date=201512&json"""
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='M')
    expenses = Column(Float)  # id_api = gf_budgetee_total & mcr200p=CBU &
    borrowed = Column(Float)  # id_api = gf_budgtfd_401000 & mcr200p=CBU
    tax_revenue = Column(Float)  # id_api = gf_budgtr_10000000 & mcr200p=CBU
    gifts = Column(Float) #id_api = gf_budgtr_42000000 & mcr200p=CBU
    total_revenue = Column(Float)  # id_api = gf_budgtr_Total_1 & mcr200p=CBU
    total_budget = Column(Float)  # id_api = gf_budgtfd_total & mcr200p=CBU

    def __repr__(self):
        return f'<Budget(dt={self.dt}, freq={self.freq}, expenses={self.expenses},' \
               f'borrowed={self.borrowed}, tax_revenue={self.tax_revenue}, ' \
               f'gifts={self.gifts}, total_revenue={self.total_revenue}, ' \
               f'total_budget={self.total_budget})>'


class Res(Base):
    """https://bank.gov.ua/NBUStatService/v1/statdirectory/res?date=201708&json"""
    __tablename__ = 'res'

    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.utcnow)
    freq = Column(String(1), default='M')
    imf_res_pos = Column(Float) # id_api = RES_IMFResPosition
    off_res_assets = Column(Float)  # id_api = RES_OffReserveAssets
    foreign_cur_res = Column(Float)  # id_api = RES_ForCurrencyAssets

    def __repr__(self):
        return f'<Res(dt={self.dt}, freq={self.freq},imf_res_pos={self.imf_res_pos},' \
               f' off_res_assets={self.off_res_assets},foreign_cur_res={self.foreign_cur_res})>'













