import configparser
import os


conf = configparser.ConfigParser()
cur_path = os.path.dirname(os.path.realpath(__file__))
config_url = os.path.join(os.path.split(cur_path)[0], 'config.ini')
conf.read(config_url)


MYSQL_HOST = conf.get('mysql', 'MYSQL_HOST')
MYSQL_NAME = conf.get('mysql', 'MYSQL_NAME')
MYSQL_PORT = conf.get('mysql', 'MYSQL_PORT')
MYSQL_USER = conf.get('mysql', 'MYSQL_USER')
MYSQL_PASSWORD = conf.get('mysql', 'MYSQL_PASSWORD')

REDIS_HOST = conf.get('redis', 'REDIS_HOST')
REDIS_PORT = conf.get('redis', 'REDIS_PORT')
REDIS_DB = conf.get('redis', 'REDIS_DB')
REDIS_PASSWORD = conf.get('redis', 'REDIS_PASSWORD')
