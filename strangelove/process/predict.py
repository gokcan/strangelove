import logging
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

from strangelove import STATIC_ROOT

logger = logging.getLogger(__name__)


class Recommendor(object):
    """ Recommends movies to the user, given the movie id. """
    _GLOBAL = 1

    def __init__(self):
      pass
        
    def read(self):
      pass


rec = Recommendor()