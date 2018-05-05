import logging
import numpy as np
import pandas as pd
from collections import OrderedDict
from scipy.sparse import csr_matrix

from strangelove import STATIC_ROOT

logger = logging.getLogger(__name__)


class FeatureAnalysis(object):
    """ Feature extraction and analysis of movielens dataset. Especially on ratings.csv """
    _GLOBAL = 1

    def __init__(self, analysis='Ratings'):
      self.analysis = analysis # In future, use this to analyze specific dataset.

    def extract(self) -> None:
      path = '{}/ratings.csv'.format(STATIC_ROOT)
      df = pd.read_csv(path)
      mean = df['rating'].mean()
      df = df[['movieId', 'rating']].groupby('movieId').agg(['mean', 'count'])
      df.rename(columns={'mean': 'vote_average', 'count': 'vote_count'}, inplace=True)
      df.columns = df.columns.droplevel(0)
      df = df.round(3).sort_values(['movieId', 'vote_count', 'vote_average'])
      
      df.to_csv('agg_movie_ratings.csv', encoding='utf-8')
      print('Aggregated movie ratings have been successfully saved!')
      print('Global vote average (C) is {}'.format(np.around(mean, decimals=3)))
      

data = FeatureAnalysis()
data.extract()
