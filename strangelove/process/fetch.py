import logging
import requests
from strangelove import API_KEY, REQUEST_URL, API_VERSION

logger = logging.getLogger(__name__)


class Movie(object):
    """ Fetches movie information from TMDB API with given movie_id. """
    _SLUG = {
        'general': '/{id}',
    }
    _APPENDED = 'credits,keywords' # Add what you want to append to response here.

    def __init__(self):
        self.base_url = '{}{}/movie'.format(REQUEST_URL, API_VERSION)
        self._payload = { 'api_key': API_KEY }
        self._payload['append_to_response'] =  self._APPENDED
        

    def fetch(self, id: int) -> dict:
        id_path = self._SLUG['general'].format(id=id)
        path = '{}{}'.format(self.base_url, id_path)
        result = requests.get(path, params=self._payload)
        return result.json()
