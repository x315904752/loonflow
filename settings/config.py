import configparser
import os


conf = configparser.ConfigParser()
cur_path = os.path.dirname(os.path.realpath(__file__))
config_url = os.path.join(os.path.split(cur_path)[0], 'config.ini')
conf.read(config_url)


def getvalue_from_env(env_name, section, option, default_value):
    value = os.environ.get(env_name, None)
    if value:
        return value
    else:
        try:
            return conf.get(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError):
            return default_value


MYSQL_HOST = getvalue_from_env('MYSQL_HOST', 'mysql', 'MYSQL_HOST', '127.0.0.1')
MYSQL_NAME = getvalue_from_env('MYSQL_NAME', 'mysql', 'MYSQL_NAME', 'loonflow')
MYSQL_PORT = getvalue_from_env('MYSQL_PORT', 'mysql', 'MYSQL_PORT', 3306)
MYSQL_USER = getvalue_from_env('MYSQL_USER', 'mysql', 'MYSQL_USER', 'root')
MYSQL_PASSWORD = getvalue_from_env('MYSQL_PASSWORD', 'mysql', 'MYSQL_PASSWORD', '')

REDIS_HOST = getvalue_from_env('REDIS_HOST', 'redis', 'REDIS_HOST', '127.0.0.1')
REDIS_PORT = getvalue_from_env('REDIS_PORT', 'redis', 'REDIS_PORT', 6379)
REDIS_DB = getvalue_from_env('REDIS_DB', 'redis', 'REDIS_DB', 0)
REDIS_PASSWORD = getvalue_from_env('REDIS_PASSWORD', 'redis', 'REDIS_PASSWORD', '')

