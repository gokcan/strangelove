import logging
import numpy as np
import pandas as pd
from collections import OrderedDict
from scipy.sparse import csr_matrix

from strangelove import STATIC_ROOT

logger = logging.getLogger(__name__)


class FeatureAnalysis(object):
    """ Feature extraction and analysis of movielens dataset. Especially on ratings.csv """
    _PATH = '{}/ratings.csv'.format(STATIC_ROOT)

    def __init__(self, analysis='Ratings', path=_PATH):
        self.analysis = analysis  # In future, use this to analyze specific dataset.
        self.path = path
        self._df = pd.read_csv(path)

    def aggregate_ratings(self) -> None:
        df = self._df[['movieId', 'rating']].groupby('movieId').agg(['mean', 'count'])
        df.rename(columns={'mean': 'vote_average', 'count': 'vote_count'}, inplace=True)
        df.columns = df.columns.droplevel(0)
        df = df.round(3).sort_values(['movieId', 'vote_count', 'vote_average'])

        df.to_csv('agg_movie_ratings.csv', encoding='utf-8')
        print('Aggregated movie ratings have been successfully saved!')

    def max(self, kind='movieId') -> int:
        return self._df[kind].max()

    def global_mean(self) -> float:
        return np.around(self._df['rating'].mean(), decimals=3)



analysis = FeatureAnalysis()
analysis.aggregate_ratings()

print('Max movie_id {}'.format(analysis.max()))
print('Global vote average (C) is {}'.format(analysis.global_mean()))
