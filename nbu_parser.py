import requests
import xml.etree.ElementTree as ET
import os

class NBUParser:

    def __init__(self, url_base, page, date, suffix):
        self.url_base = url_base
        self.page = page
        self.date = date
        self.suffix = suffix

    def get_json(self):
        date = f'date={self.date}'
        url = os.path.join(self.url_base, self.page) + f'?{date}{self.suffix}'
        response = requests.get(url)
        return response.json()

class ExchangeParser(NBUParser):

    def __init__(self, url_base, page, date, suffix):
        super().__init__(url_base, page, date, suffix)
        self.date = date
        self.page = page

    def parse_exchange(self):
        json_data = self.get_json()
        print(*json_data, sep='\n')

base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory"
print(ExchangeParser(base_url, 'exchange', '20181126', '&json').parse_exchange())


class GrossExtDebtParser(NBUParser):
    pass


#TODO: Add as many classes, as required

e = ExchangeParser('https://bank.gov.ua/NBUStatService/v1/statdirectory', 'exchange?date=20181116&json', 'joj', 'joj')
print(e.parse_exchange())