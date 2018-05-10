import numpy as np
import pandas as pd

from strangelove.engine import base
from strangelove.process.util import MatrixUtility
from strangelove import STATIC_ROOT


class ContentBasedRecommender(base.Recommender):
    """
      Content-Based Recommender for movies. 

    """
    _PATH = '{}/meta.csv'.format(STATIC_ROOT)

    def __init__(self, utility=MatrixUtility):
        self.utility = utility()
        self.csr = None
        self.path = self._PATH
        self.df = pd.read_csv(self.path)

    def recommend(self, user_id: int, size: int=10) -> list:
        """Recommends movie to specific user.
        :type id: int
        :param id: user id according to the recommender type

        :type size: int
        :param size: number of recommendations

        """

    def similar_items(self, item_id, size: int=10) -> list:
        """Returns similar items of the given item.
        :type id: int
        :param id: item id according to the recommender type

        :type size: int
        :param size: number of recommendations

        """
        cast_csr = self.utility.load_csr_matrix(field_name='cast')
        director_csr = self.utility.load_csr_matrix(field_name='director')
        genre_csr = self.utility.load_csr_matrix(field_name='genre')
        keyword_csr = self.utility.load_csr_matrix(field_name='keyword')

        cast, director, genre, keywords= cast_csr[item_id], director_csr[item_id], genre_csr[item_id], keyword_csr[item_id]

        cm_cast = self._contentwise_similar(cast.indices, cast_csr)
        cm_director = self._contentwise_similar(director.indices, director_csr)
        cm_genre = self._contentwise_similar(genre.indices, genre_csr)
        cm_keywords = self._contentwise_similar(keywords.indices, keyword_csr)

        similar_items = []
        for movie_id, similarity in enumerate(zip(cm_cast, cm_director, cm_genre, cm_keywords), 1):
            cast, director, genre, keyword = similarity
            sim_score = cast*0.2 + director*0.3 + genre*0.2 + keyword*0.3
            similar_items.append((movie_id, self.movie_name(movie_id), 'confidence: {}'.format(sim_score)))

        similar_items.sort(key=lambda v: v[2], reverse=True)

        return similar_items[1:size+1]  # Most similar one equals to itself, so don't return it.

    def _contentwise_similar(self, current, util_content_csr):
        similarities = []
        length = util_content_csr.shape[0]
        for movie in range(1, length):
            values = util_content_csr[movie].indices
            #if values.size: 
            similarities.append(self.utility.jaccard_similarity_score(current, values))

        return similarities

    def movie_name(self, movieId=1):
        k = self.df.loc[self.df['movieId'] == movieId, 'title']
        return k.iloc[0] if k.any() else ""


cb = ContentBasedRecommender()
print(cb.similar_items(55232, 3)) # 1036, Die Hard (1988)