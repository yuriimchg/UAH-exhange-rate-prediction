import requests
import xml.etree.ElementTree as ET
import os

class NBUParser:

    def __init__(self, url_base, db_uri, date):
        self.url_base = url_base
        self.db_uri = db_uri
        self.date = date


class ExchangeParser(NBUParser):

    def __init__(self, url_base, url_suffix, db_uri, date):
        self.url_suffix = url_suffix
        self.url_base = url_base
        self.db_uri = db_uri
        self.date = date

    def get_json(self):
        url = os.path.join(self.url_base, self.url_suffix)
        response = requests.get(url)
        return response.json()

    def parse_exchange(self):
        
        json_data = self.get_json()
        print(json_data)


class GrossExtDebtParser(NBUParser):
    pass


#TODO: Add as many classes, as required

e = ExchangeParser('https://bank.gov.ua/NBUStatService/v1/statdirectory', 'exchange?date=20181116&json', 'joj', 'joj')
print(e.parse_exchange())