
from strangelove.engine import base
import strangelove.process.reader
from strangelove.process.util import MatrixUtility, _save_csr_matrix
from strangelove.utility.cosine_similarity import CosineSimilarity
from strangelove.utility.tfidf_similarity import TFIDFSimilarity
from strangelove.utility.matrix_factorization import MatrixFactorization
import pandas as pd
from strangelove import STATIC_ROOT

from scipy.sparse import csr_matrix, csc_matrix, coo_matrix
import numpy as np
from os.path import exists


class ItemBasedRecommender(base.Recommender):
    """
      Item-Item Recommender for movies.
    """
    _PATH = '{}/meta.csv'.format(STATIC_ROOT)

    def __init__(self, utility=MatrixUtility):
        self.utility = utility()
        self.tag_csr = None
        self.rating_csr = None
        self.rating_similarity_matrix = None
        self.tag_similarity_matrix = None
        self.similarity_matrix = None
        self.df = pd.read_csv(self._PATH)

    def load_csr_matrix(self,  metric_type='rating', regenerate=False):
        "Loads sparse csv"
        self.metric_type = metric_type
        if metric_type == 'rating':
            self._load_rating_csr(regenerate) 
        elif metric_type == 'tag':
            self._load_tag_csr(regenerate)
        else:
            self._load_rating_csr(regenerate)  
            self._load_tag_csr(regenerate)

    def _load_tag_csr(self, regenerate=False):
        if not _check_csr('tag') or regenerate:
            self.utility.build_user_tag_csr()
        npz = np.load('tag-csr.npz')
        self.tag_csr = csr_matrix((npz["data"], npz["indices"],
                                npz["indptr"]), shape=npz["shape"])

    def _load_rating_csr(self, regenerate=False):
        if not _check_csr('rating') or regenerate:
            self.utility.build_user_rating_csr()
        npz = np.load('rating-csr.npz')
        self.rating_csr = csr_matrix((npz["data"], npz["indices"],
                                npz["indptr"]), shape=npz["shape"])

    def similar_items(self, item_id=2692, size=10):
        if size >= self.similarity_matrix.shape[0]:
            return []
        return sorted(
            list(self._iter_np(self.similarity_matrix, item_id)), key=lambda x: -x[1])[:size]


    def _iter_np(self, m, row):
        for index in range(m.indptr[row], m.indptr[row+1]):
            yield self.movie_name(m.indices[index]), m.data[index]

    def preprocess(self, model_name='cosine', rating_sim_constraint=0.6, prediction=True, regenerate=False):
        """Trains the dataset and creates similarity matrix according to similarity model.
        :type model_name: str
        :param model_name: Applied model name.
        """
        if prediction:
            self._apply_prediction(metric_type=self.metric_type, regenerate=regenerate)

        else:
            if self.tag_csr is not None:
                model = self._apply_tag_similarity(model_name, regenerate)
                self.tag_similarity_matrix = model.train()

            if self.rating_csr is not None:
                model = self._apply_rating_similarity(model_name, regenerate)                
                self.rating_similarity_matrix = model.train()
        

        if self.rating_similarity_matrix is not None and self.tag_similarity_matrix is not None:
            tag_matrix = np.dot(self.tag_similarity_matrix, 1 - rating_sim_constraint)
            rate_matrix = np.dot(self.rating_similarity_matrix, rating_sim_constraint)
            self.similarity_matrix = tag_matrix + rate_matrix
        else:
            self.similarity_matrix = self.rating_similarity_matrix if self.rating_similarity_matrix is not None \
                                                                    else self.tag_similarity_matrix             

    def _apply_prediction(self, metric_type: str, regenerate=False):
        if metric_type == 'rating': 
            self._predict_rating(regenerate)
        elif metric_type == 'tag':
            self._predict_tag(regenerate)
        else:
            self._predict_rating(regenerate)
            self._predict_tag(regenerate)


    def _predict_rating(self, regenerate=False):
        if not _check_csr('rating-predicted') or regenerate:
            mf = MatrixFactorization(self.rating_csr.toarray())
            mf.train()
            self.rating_similarity_matrix = cosine_similarity(mf)
            _save_csr_matrix(csr=self.rating_similarity_matrix, field_type='rating-predicted-similarity')
        else:
            npz = np.load('rating-predicted-csr.npz')
            self.rating_similarity_matrix = csr_matrix((npz["data"], npz["indices"],
                                    npz["indptr"]), shape=npz["shape"])

    def _predict_tag(self, cosine_similarity, regenerate=False):
        if not _check_csr('tag-predicted-similarity') or regenerate:
            mf = MatrixFactorization(self.tag_csr.toarray())
            mf.train()
            self.tag_similarity_matrix = cosine_similarity(mf)
            _save_csr_matrix(csr=self.tag_similarity_matrix, field_type='tag-predicted-similarity')
        else:
            npz = np.load('tag-predicted-similarity-csr.npz')
            self.tag_similarity_matrix = csr_matrix((npz["data"], npz["indices"],
                                    npz["indptr"]), shape=npz["shape"])

    def _apply_rating_similarity(self, model_name: str, regenerate=False):
        if model_name == 'cosine':
            model = CosineSimilarity(self.rating_csr)
        elif model_name == 'tfidf':
            model = TFIDFSimilarity(self.rating_csr)
        else:
            raise Exception("Unsupported similarity model")
        return model

    def _apply_tag_similarity(self, model_name: str, regenerate=False):
        if model_name == 'cosine':
            model = CosineSimilarity(self.tag_csr)
        elif model_name == 'tfidf':
            model = TFIDFSimilarity(self.tag_csr)
        else:
            raise Exception("Unsupported similarity model")
        return model

    def recommend(
            self, 
            user_id,
            size: int=10, 
            tag_sim_constraint=0.0015, 
            rating_sim_constraint=4) -> list:
        """Recommends movie.
        :type user_id: int
        :param id: ID of user.
        :type size: int
        :param size: Size of list to return
        returns lists of recommended movies.
        """
        similar_movies = list()
        if self.metric_type in ['rating', 'combined']:
            user_ratings = self.rating_csr[user_id]
            for index, data in zip(user_ratings.indices, user_ratings.data):
                if data >= rating_sim_constraint:
                    similar_movies += self.similar_items(item_id=index, size=5)

        if self.metric_type in ['tag', 'combined']:
            user_tags = self.tag_csr[user_id]
            for index, data in zip(user_tags.indices, user_tags.data):
                if data >= tag_sim_constraint:
                    similar_movies += self.similar_items(item_id=index, size=10)
        unique_movies = set(similar_movies)
        return sorted(list(unique_movies), key=lambda x: -x[1])[:size]


    def movie_name(self, movieId=1):
        k = self.df.loc[self.df['movieId'] == movieId, 'title']
        return k.iloc[0] if k.any() else ""


def cosine_similarity(model: MatrixFactorization):
    # out of memory
    sim = model.item_factors.dot(model.item_factors.T)
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return sim / norms / norms.T

def _check_csr(field_type):
    csr_name = '{}{}'.format(field_type, '-csr.npz')
    csc_name = '{}{}'.format(field_type, '-csc.npz')
    if exists(csr_name) and exists(csc_name):
        return True
    return False

cf = ItemBasedRecommender()
cf.load_csr_matrix(metric_type='combined')
cf.preprocess(regenerate=True, prediction=False)
print(cf.similar_items(153))
print(cf.recommend(1))