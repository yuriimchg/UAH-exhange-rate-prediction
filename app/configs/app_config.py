import os
basedir = os.path.abspath(os.path.dirname(__file__))


DB_CONFIG_DICT = {'user' : 'yurii',
                  'password' : 'asreliableas12345',
                  'host' : 'localhost',
                  'port' : '5432'}
SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://{}:{}@{}:{}'.format(*DB_CONFIG_DICT.values())

SQLALCHEMY_TRACK_MODIFICATIONS = False