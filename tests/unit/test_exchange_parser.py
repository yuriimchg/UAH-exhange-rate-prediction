from app.nbu_parser import ExchangeParser, base_url
from datetime import datetime

parser = ExchangeParser(base_url, '20110401')

def test_exchange_url_ok():
    assert parser.get_url() == 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date=20110401&&json'

def test_exchange_json_ok():
    assert len(parser.get_json()) > 0
    assert parser.get_json()[1]['r030'] == 36
    assert parser.get_json()[2]['cc'] == 'CAD'



def test_exchange_json_keys():
    keys = ['r030', 'txt', 'rate', 'cc', 'exchangedate']
    assert list(parser.get_json()[3].keys()) == keys