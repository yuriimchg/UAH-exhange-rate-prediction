import requests
import json
import os


class NBUParser:

    def __init__(self, url_base, page, date, params={}, suffix='json'):
        self.url_base = url_base
        self.page = page
        self.date = date
        self.params = params
        self.suffix = suffix

    def get_url(self):
        date = f'date={self.date}'
        base_url = os.path.join(self.url_base, self.page)
        params_str = '&'.join([f'{k}={v}' for k, v in self.params.items()])
        return base_url + f'?{date}&{params_str}&{self.suffix}'

    def get_json(self):
        """ Get json data from the requested URL"""
        response = requests.get(self.get_url())
        return response.json()

    def __repr__(self):
        return self.get_url()


class ExchangeParser(NBUParser):

    def __init__(self, url_base, page, date, suffix):
        super().__init__(url_base, page, date, suffix)
        self.date = date
        self.page = page

    def parse_exchange(self):
        json_data = self.get_json()
        print(*json_data, sep='\n')


class MonetaryParser(NBUParser):

    def __init__(self, url_base, page, date, suffix, params):
        super().__init__(url_base, page, date, suffix, params)
        self.page = page
        self.date = date
        self.suffix = suffix
        self.params = params

    def parse_monetary(self):
        json_data = self.get_json()
        print(json_data)


class BanksIncExParser(NBUParser):

    def __init__(self, url_base, page, date, suffix, params):
        super().__init__(url_base, page, date, suffix, params)
        self.page = page
        self.date = date
        self.suffix = suffix
        self.params = params

    def parse_banks(self):
        json_data = self.get_json()
        print(json_data)


class InvestmentParser(NBUParser):

    def __init__(self, url_base, page, date, suffix, params):
        super().__init__(url_base, page, date, suffix, params)
        self.page = page
        self.date = date
        self.suffix = suffix
        self.params = params

    def parse_investment(self):
        json_data = self.get_json()
        print(json_data)


class GrossExtDebtParser(NBUParser):

    def __init__(self, url_base, page, date, suffix, params):
        super().__init__(url_base, page, date, suffix, params)
        self.page = page
        self.date = date
        self.suffix = suffix
        self.params = params

    def parse_ged(self):
        json_data = self.get_json()
        print(json_data)




# TODO: Add as many classes, as required

base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory"  ###########
# print(ExchangeParser(base_url, 'exchange', '20181126', '&json').parse_exchange())  ###########
print(NBUParser(base_url, 'grossextdebt', '200401', {'id_api':'ed'}))   ########################
print(NBUParser(base_url, 'exchange', '200401'))        ########################################
# e = ExchangeParser('https://bank.gov.ua/NBUStatService/v1/statdirectory', 'exchange?date=20181116&json', 'joj', 'joj')
#
# print(e.parse_exchange())

