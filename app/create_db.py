from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from configs.app_config import SQLALCHEMY_DB_URI
from datetime import date

# Import tables
from db_models import Exchange, Monetary, BanksIncomesExpenses, Investment, GrossExtDebt
from db_models import EconomicActivity, Budget, Res, Inflation


def create_db(db_uri=SQLALCHEMY_DB_URI):
    """ Create new database if it does not exist """
    assert not database_exists(db_uri)
    create_database(db_uri, encoding='utf8')


def create_tables(db_uri = SQLALCHEMY_DB_URI):
    engine = create_engine(db_uri, echo=True)



