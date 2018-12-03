import requests
import os
from app import app, db

from app.db_models import Exchange, Monetary, BanksIncomesExpenses, Investment, GrossExtDebt
from app.db_models import EconomicActivity, Budget, Res, Inflation


class NBUParser:
    """ Base class for parsing bank.gov.ua API """

    def __init__(self, base, page, start_date, params={}, suffix='json'):
        self.base = base
        self.page = page
        self.start_date = start_date
        self.params = params
        self.suffix = suffix

    def get_url(self, date):
        base_url = os.path.join(self.base, self.page)
        params_str = '&'.join([f'{k}={v}' for k, v in self.params.items()])
        return base_url + f'?{date}&{params_str}&{self.suffix}'

    def get_json(self, date):
        """ Get json data from the requested URL"""
        response = requests.get(self.get_url(date))
        return response.json()


class ExchangeParser(NBUParser):

    def __init__(self, base):
        super().__init__(base, 'exchange', '19980101', {}, 'json')

        self.url = NBUParser(self.base, self.page,
                             self.start_date, self.params,
                             self.suffix).get_url(self.start_date)

    def add_exchanges_to_db(self, date):
        json_data = self.get_json(date)
        for currency in json_data:
            cur = Exchange(
                r030=currency['r030'],
                exchangedate=currency['exchangedate'],
                txt=currency['txt'],
                rate=currency['rate'],
                cc=currency['cc'])
            db.session.add(cur)
            db.session.commit()
        return f'Added exchange rates for {date} to database'


class MonetaryParser(NBUParser):

    def __init__(self, base, params):
        super().__init__(base, 'monetary', '20030201', params, 'json')
        self.params = params
        self.url = NBUParser(self.base, self.page,
                             self.start_date, self.params,
                             self.suffix).get_url(self.start_date)

    def add_monetary_to_db(self, date):
        json_data = self.get_json(date)



class BanksIncExParser(NBUParser):

    def __init__(self, base, date, params):
        super().__init__(base, 'banksincexp', date, params, 'json')
        self.params = params
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()

    def parse_banks(self):
        json_data = self.get_json()
        print(json_data)


class InvestmentParser(NBUParser):

    def __init__(self, base, date, params):
        super().__init__(base, 'interinvestpos', date, params, 'json')
        self.params = params
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()

    def parse_investment(self):
        json_data = self.get_json()
        print(json_data)


class GrossExtDebtParser(NBUParser):

    def __init__(self, base, date, params):
        super().__init__(base, 'grossextdebt', date, params, 'json')
        self.params = params
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()

    def parse_ged(self):
        json_data = self.get_json()
        print(json_data)


class InflationParser(NBUParser):

    def __init__(self, base, date, params):
        super().__init__(base, 'inflation', date, params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()
        
    def parse_inflation(self):
        json_data = self.get_json()
        print(json_data)


class EconomicActivityParser(NBUParser):
    
    def __init__(self, base, date, params):
        super().__init__(base, 'economicactivity', date, params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()
        
    def parse_activity(self):
        json_data = self.get_json()
        print(json_data)


class BudgetParser(NBUParser):

    def __init__(self, base, date, params):
        super().__init__(base, 'budget', date, params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()

    def parse_budget(self):
        #json_data = self.get_json()
        print(self.url)


class ResParser(NBUParser):

    def __init__(self, base, date, params):
        super().__init__(base, 'res', date, params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()

    def parse_res(self):
        json_data = self.get_json()
        print(json_data)




# TODO: Add as many classes, as required

base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory"  ###########
print(ExchangeParser(base_url, '20181126').parse_exchange())  ###########
# # print(NBUParser(base_url, 'grossextdebt', '200401', {'id_api':'ed'}))   ########################
# # print(NBUParser(base_url, 'exchange', '200401'))        ########################################
# e = ExchangeParser('https://bank.gov.ua/NBUStatService/v1/statdirectory', 'exchange?date=20181116&json', 'joj', 'joj')
# #
# # print(e.parse_exchange())
#
# #print(ResParser(base_url, '20181126', params={'id_api' : 'RES_IMFResPosition'}).parse_res())
# print(BudgetParser(base_url, '20120101', params={'id_api' : 'gf_budgtr_10000000',
#                                                  'mcr200p' : 'CBU',
#                                                  'period' : 'm'}).parse_budget())
#
