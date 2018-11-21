# TODO: Add Google Trands parser DAG
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime, timedelta

# Import tables
from db_models import Exchange, Monetary, BanksIncomesExpenses, Investment, GrossExtDebt, Inflation
from db_models import EconomicActivity, Budget, Res

# Import API parser
from nbu_parser import ExchangeParser

######################################################################
# TODO Airflow DAG that has nodes:
# 1. Create database if not exists
# 2. Set the date and parameters for url with respect of url parameters. Set the initial date if database hasn't existed before
# 3. Parse JSONS & get the data
# 4. Insert data into the database

#   (1) -> (2) -> (3) -> (4)
######################################################################

default_args = {
        'owner' : 'Yurii',
        'depends_on_past' : False,
        'start_date' : datetime(2001,1,1), # TODO: insert start_date,
        'retries' : 1,
        'retry_delay' : None,
}
# DAG
parsing_dag = DAG('parsing_dag', start_date=datetime(2001, 1, 1))

# Tasks:

