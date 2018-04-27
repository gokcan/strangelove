import logging
import requests
from strangelove import API_KEY, REQUEST_URL, API_VERSION

logger = logging.getLogger(__name__)


class Movie(object):
    """ Fetches movie information from TMDB API with given movie_id. """
    SLUG = {
        'general': '/{id}',
    }

    def __init__(self):
        self.base_url = '{}{}/movie'.format(REQUEST_URL, API_VERSION)
        self._payload = {'api_key': API_KEY, 'append_to_response': 'credits'}

    def fetch(self, id):
        id_path = self.SLUG['general'].format(id=id)
        path = '{}{}'.format(self.base_url, id_path)
        result = requests.get(path, params=self._payload)
        return result.json()


movie = Movie()

# TODO: Change this to iterate over tmdb_ids located in links.csv
for i in range(10):
    if 'status_code' in movie.fetch(i):
        value = movie.fetch(i)['status_code']
        logger.log(1, value)
    else:  # status_code is not set for successful read operations.
        print(movie.fetch(i))  # TODO: Write to a new csv file.
