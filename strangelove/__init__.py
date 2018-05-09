import configparser
import os
import pkgutil

__path__ = pkgutil.extend_path(__path__, __name__)
__LOCATION__ = os.path.dirname(os.path.abspath(__file__))

# APP CONF
_config = configparser.ConfigParser()
_config.read('{}/conf/config.ini'.format(__LOCATION__))

API_KEY = _config['tmdb']['api_key']
API_VERSION = _config['tmdb']['api_version']
REQUEST_URL = _config['tmdb']['request_url']
DATASET_SIZE = _config['movielens']['size']

# STATIC ROOT
STATIC_ROOT = '{}/dataset/movielens/{}'.format(__LOCATION__, DATASET_SIZE)
