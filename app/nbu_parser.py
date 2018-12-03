import requests
import os
from app import app


class NBUParser:
    """ Base class for parsing bank.gov.ua API """

    def __init__(self, base, page, date, params={}, suffix='json'):
        self.base = base
        self.page = page
        self.date = date
        self.params = params
        self.suffix = suffix

    def get_url(self):
        date = f'date={self.date}'
        base_url = os.path.join(self.base, self.page)
        params_str = '&'.join([f'{k}={v}' for k, v in self.params.items()])
        return base_url + f'?{date}&{params_str}&{self.suffix}'

    def get_json(self):
        """ Get json data from the requested URL"""
        response = requests.get(self.get_url())
        return response.json()


class ExchangeParser(NBUParser):

    def __init__(self, base, date):
        super().__init__(base, 'exchange', date, {}, 'json')
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()

    def parse_exchange(self):
        json_data = self.get_json()
        print(*json_data, sep='\n')


class MonetaryParser(NBUParser):

    def __init__(self, base, date, params):
        super().__init__(base, 'monetary', date, params, 'json')
        self.params = params
        self.url = NBUParser(self.base, self.page, self.date,
                             self.params, self.suffix).get_url()

    def parse_monetary(self):
        json_data = self.get_json()
        print(json_data)


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

# base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory"  ###########
# print(ExchangeParser(base_url, '20181126').parse_exchange())  ###########
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
