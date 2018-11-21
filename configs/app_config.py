DB_CONFIG_DICT = {'user' : 'yurii',
                  'password' : 'asreliableas12345',
                  'host' : 'localhost',
                  'port' : '5434'}
SQLALCHEMY_DB_URI = 'psycopg2+postgresql://{}:{}@{}:{}'.format(*DB_CONFIG_DICT.values())

print(SQLALCHEMY_DB_URI)
