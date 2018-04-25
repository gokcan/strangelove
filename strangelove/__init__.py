import configparser
import os
import pkgutil

__path__ = pkgutil.extend_path(__path__, __name__)
__LOCATION__ = os.path.dirname(os.path.abspath(__file__))

# APP CONF
_config = configparser.ConfigParser()
_config.read('{}/conf/config.ini'.format(__LOCATION__))

API_KEY = _config['tmdb']['api_key']
REQUEST_URL = _config['tmdb']['request_url']

# STATIC ROOT
STATIC_ROOT = '{}/dataset/movielens/100k'.format(__LOCATION__)
