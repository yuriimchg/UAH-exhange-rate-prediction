import requests
import os
from datetime import datetime
from app import app, db
from app.db_models import Exchange, Monetary, BanksIncomesExpenses, Investment, GrossExtDebt
from app.db_models import EconomicActivity, Budget, Res, CoreInflation, ConsumerPriceIndices

# TODO: add params to class instances

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

    def filter_by_params(self, json_string, filter_args):
        """ Filter response by parameters """
        for key, val in filter_args:
            json_string = list(filter(lambda x: x[key] == val, json_string))
        return json_string[0]['value']


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
                exchangedate=datetime.strptime(currency['exchangedate'], '%d.%m.%Y'),
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
        monthly_monetary = Monetary(
            dt=datetime.strptime(date, '%Y%m%d'),
            m0_cash=self.filter_by_params(json_data, {'id_api': 'M0'}),
            m1_aggregate=self.filter_by_params(json_data, {'id_api': 'M1'}),
            m2_aggregate=self.filter_by_params(json_data, {'id_api': 'M2'}),
            m3_aggregate=self.filter_by_params(json_data, {'id_api': 'M3'})
        )
        db.session.add(monthly_monetary)
        db.session.commit()
        return f'Added monetary for {date} to database'


class BanksIncExParser(NBUParser):

    def __init__(self, base, params):
        super().__init__(base, 'banksincexp', '20090201', params, 'json')
        self.params = params
        self.url = NBUParser(self.base, self.page, self.start_date,
                             self.params, self.suffix).get_url()

    def add_banks_to_db(self, date):
        json_data = self.get_json(date)
        one_day_balance = BanksIncomesExpenses(
            dt=datetime.strptime(date, '%Y%m%d'),
            m3_aggregate=self.filter_by_params(json_data, {'id_api': 'M3'}),
            total_income=self.filter_by_params(json_data, {'id_api': 'BS2_IncomeTotal'}),
            total_expense=self.filter_by_params(json_data, {'id_api': 'BS2_ExpensesTotal'}),
            income_tax=self.filter_by_params(json_data, {'id_api': 'BS2_ExpTaxIncome'}),
            net_profit=self.filter_by_params(json_data, {'id_api': 'BS2_NetProfitLoss'})
        )
        db.session.add(one_day_balance)
        db.session.commit()
        return f'Added monthly banks incomes and expences for {date} to database'


class InvestmentParser(NBUParser):

    def __init__(self, base, params):
        super().__init__(base, 'interinvestpos', '20030101', params, 'json')
        self.params = params
        self.url = NBUParser(self.base, self.page, self.start_date,
                             self.params, self.suffix).get_url(self.start_date)

    def add_investment_to_db(self, date):
        json_data = self.get_json(date)
        monthly_investment = Investment(
            dt=datetime.strptime(date, '%Y%m%d'),
            net_profit=self.filter_by_params(json_data, {'id_api': 'BS2_NetProfitLoss'}),
            assets=self.filter_by_params(json_data, {'id_api': 'IIP_NET', 's181': 'Total'}),
            net_inv_pos=self.filter_by_params(json_data, {'id_api': 'IIP_Net', 's181': 'Total'}),
            direct_inv=self.filter_by_params(json_data, {'id_api': 'FDI_A', 's181': 'Total'})
        )
        db.session.add(monthly_investment)
        db.session.commit()
        return f'Added investment for {date} to database'


class GrossExtDebtParser(NBUParser):

    def __init__(self, base, params):
        super().__init__(base, 'grossextdebt', '20040101', params, 'json')
        self.params = params
        self.url = NBUParser(self.base, self.page, self.start_date,
                             self.params, self.suffix).get_url(self.start_date)

    def add_ged_to_db(self, date):
        json_data = self.get_json(date)
        q_ged = GrossExtDebt(
            dt=datetime.strptime(date, '%Y%m%d'),
            grossextdebt=self.filter_by_params(json_data, {'id_api': 'ED'})
        )
        db.session.add(q_ged)
        db.session.commit()
        return f'Added GrossExtDebt for {date} to database'


class CoreInflationParser(NBUParser):

    def __init__(self, base, params):
        super().__init__(base, 'inflation', '20080201', params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.start_date,
                             self.params, self.suffix).get_url(self.start_date)
        
    def add_inflation_to_db(self, date):
        json_data = self.get_json(date)
        core_inf = CoreInflation(
            dt=datetime.strptime(date, '%Y%m%d'),
            consumer_price_index_dtpy=self.filter_by_params(json_data,
                                {'id_api': 'prices_price_ci_',
                                 'mcrd081': 'Total',
                                 'period': 'm',
                                 'tzep': 'dtpy_'}),
            consumer_price_index_pcpm=self.filter_by_params(json_data,
                                {'id_api': 'prices_price_ci_',
                                 'mcrd081': 'Total',
                                 'period': 'm',
                                 'tzep': 'pcpm_'}),
            consumer_price_index_pccm=self.filter_by_params(json_data,
                                {'id_api': 'prices_price_ci_',
                                 'mcrd081': 'Total',
                                 'period': 'm',
                                 'tzep': 'pccm_'}),
            consumer_price_index_pccp=self.filter_by_params(json_data,
                                {'id_api': 'prices_price_ci_',
                                 'mcrd081': 'Total',
                                 'period': 'm',
                                 'tzep': 'pccp_'}))
        db.session.add(core_inf)
        db.session.commit()
        return f'Added core inflation to for {date} database'


class CPIParser(NBUParser):

    def __init__(self, base, params):
        super().__init__(base, 'inflation', '20070201', params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.start_date,
                             self.params, self.suffix).get_url(self.start_date)

    def add_cpi_to_db(self, date):
        json_data = self.get_json(date)
        for json_string in json_data:
            consumer_price_indices = ConsumerPriceIndices(
                dt=datetime.strptime('%Y%m%d'),
                ku=json_string['ku'],
                tzep=json_string['tzep'],
                price_cpi=json_string['value'])
            db.session.add(consumer_price_indices)
            db.session.commit()
        return f'Successfully added raw consumer price indices to database for date={date}'


class EconomicActivityParser(NBUParser):
    
    def __init__(self, base, params):
        super().__init__(base, 'economicactivity', '20100201', params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.start_date,
                             self.params, self.suffix).get_url(self.start_date)
        
    def parse_activity(self, date):
        json_data = self.get_json(date)
        filtered_args = {'tzep': 'F_', 'mcr210i': 'TOTAL', 'mcrk110': 'Total'}
        activity = EconomicActivity(
            dt=datetime.strptime(date, '%Y%m%d'),
            gross_dom_prod=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_ps_gdp_cp'}),
            gross_surplus=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_is_gross_surplus'}),
            employee_compensation=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_is_emp_comp'}),
            gross_val_added=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_ps_gv_add'}),
            gross_surplus_mixed_inc=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_is_gross_surplus'}),
            gross_fixed_cap_form=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_es_gfcf'}),
            net_export=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_es_net_exp'}),
            exports=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_es_net_egs'}),
            imports=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_es_igs'}),
            gross_cap_form=self.filter_by_params(json_data, {**filtered_args, 'id_api': 'ea_gdp_es_gf'}),
        )
        db.session.add(activity)
        db.session.commit()
        return f'Added to database economic activity data for {date}'


class BudgetParser(NBUParser):

    def __init__(self, base, params):
        super().__init__(base, 'budget', '20100201', params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.start_date,
                             self.params, self.suffix).get_url(self.start_date)

    def parse_budget(self, date):
        json_data = self.get_json(date)
        budget = Budget(
            dt=datetime.strptime(date, '%Y%m%d'),
            expenses = self.filter_by_params(json_data, {'id_api': 'gf_budgetee_total', 'mcr200p': 'CBU'}),
            borrowed = self.filter_by_params(json_data, {'id_api': 'gf_budgtfd_401000', 'mcr200p': 'CBU'}),
            tax_revenue = self.filter_by_params(json_data, {'id_api': 'gf_budgtr_10000000', 'mcr200p': 'CBU'}),
            gifts = self.filter_by_params(json_data, {'id_api': 'gf_budgtr_42000000', 'mcr200p': 'CBU'}),
            total_revenue = self.filter_by_params(json_data, {'id_api': 'gf_budgtr_Total_1', 'mcr200p': 'CBU'}),
            total_budget = self.filter_by_params(json_data, {'id_api': 'gf_budgtfd_total', 'mcr200p': 'CBU'}),
        )
        db.session.add(budget)
        db.session.commit()
        return f'Added budget data for {date} to database'


class ResParser(NBUParser):

    def __init__(self, base, params):
        super().__init__(base, 'res', '20030201', params)
        self.params = params
        self.url = NBUParser(self.base, self.page, self.start_date,
                             self.params, self.suffix).get_url(self.date)

    def parse_res(self, date):
        json_data = self.get_json(date)
        res = Res(
            dt=datetime.strptime(date, '%Y%m%d'),
            imf_res_pos = self.filter_by_params(json_data, {'id_api': 'RES_IMFResPosition'}),
            off_res_assets = self.filter_by_params(json_data, {'id_api': 'RES_OffReserveAssets'}),
            foreign_cur_res = self.filter_by_params(json_data, {'id_api': 'RES_ForCurrencyAssets'}),
        )
        db.session.add(res)
        db.session.commit()
        return f'Added resource data for {date} to database'


# TODO: Add as many classes, as required

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
