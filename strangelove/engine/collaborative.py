from strangelove.engine import base
import strangelove.process.reader
from strangelove.process.util import MatrixUtility
from strangelove.utility.cosine_similarity import CosineSimilarity
from strangelove.utility.tfidf_similarity import TFIDFSimilarity
from strangelove.utility.matrix_factorization import MatrixFactorization
import math

from scipy.sparse import csr_matrix, csc_matrix, coo_matrix
import numpy as np
from numpy import bincount, log, log1p, sqrt

class ItemBasedRecommender(base.Recommender):
    """
      Item-Item Recommender for movies.
    """
    def __init__(self, utility=MatrixUtility):
        self.utility = utility()
        self.tag_csr = None
        self.rating_csr = None
        self.rating_similarity_matrix = None
        self.tag_similarity_matrix = None
        self.similarity_matrix = None

    def load_csr_matrix(self,  metric_type='rating', regenerate=False):
        "Loads sparse csv"

        if metric_type == 'rating':
            self._load_rating_csr(regenerate) 
        elif metric_type == 'tag':
            self._load_tag_csr(regenerate)
        else:
            self._load_rating_csr(regenerate)  
            self._load_tag_csr(regenerate)

    def _load_tag_csr(self, regenerate=False):
        if not _check_csr('tag') and regenerate:
            self.utility.build_user_tag_csr()
        npz = np.load('tag-csr.npz')
        self.tag_csr = csr_matrix((npz["data"], npz["indices"],
                                npz["indptr"]), shape=npz["shape"])

    def _load_rating_csr(self, regenerate=False):
        if not _check_csr('tag') and regenerate:
            self.utility.build_user_rating_csr()
        npz = np.load('rating-csr.npz')
        self.rating_csr = csr_matrix((npz["data"], npz["indices"],
                                npz["indptr"]), shape=npz["shape"])

    def similar_items(self, item_id=2692, size=10):
        if size >= self.similarity_matrix.shape[0]:
            return []
        return sorted(
            list(iter_np(self.similarity_matrix, item_id)), key=lambda x: -x[1])[:size]

    def preprocess(self, model_name='cosine', rating_sim_constraint=0.6, prediction=True):
        """Trains the dataset and creates similarity matrix according to similarity model.
        :type model_name: str
        :param model_name: Applied model name.
        """
        if self.tag_csr is not None:
            model = self._apply_tag_similarity(model_name, prediction)
            self.tag_similarity_matrix = model.train()

        if self.rating_csr is not None:
            model = self._apply_rating_similarity(model_name, prediction)
            self.rating_similarity_matrix = model.train()
        

        if self.rating_similarity_matrix is not None and self.tag_similarity_matrix is not None:
            tag_matrix = np.dot(self.tag_similarity_matrix, 1 - rating_sim_constraint)
            rate_matrix = np.dot(self.rating_similarity_matrix, rating_sim_constraint)
            self.similarity_matrix = tag_matrix + rate_matrix            

    
    def _apply_rating_similarity(self, model_name: str, prediction=True):
        if prediction:
            self.rating_csr = csr_matrix(MatrixFactorization(self.rating_csr.toarray()).train())
        if model_name == 'cosine':
            model = CosineSimilarity(self.rating_csr)
        elif model_name == 'tfidf':
            model = TFIDFSimilarity(self.rating_csr)
        else:
            raise Exception("Unsupported similarity model")
        return model

    def _apply_tag_similarity(self, model_name: str, prediction=True):
        if prediction:
            self.rating_csr = csr_matrix(MatrixFactorization(self.tag_csr.toarray()).train())
        if model_name == 'cosine':
            model = CosineSimilarity(self.tag_csr)
        elif model_name == 'tfidf':
            model = TFIDFSimilarity(self.tag_csr)
        else:
            raise Exception("Unsupported similarity model")
        return model

    def recommend(self, user_id, size: int=10, similarity_constraint=0.6) -> list:
        """Recommends movie.
        :type user_id: int
        :param id: ID of user.

        :type size: int
        :param size: Size of list to return

        returns lists of recommended movies.
        """
        pass


def _check_csr(field_type):
    csr_name = '{}{}'.format(field_type, '-csr.npz')
    csc_name = '{}{}'.format(field_type, '-csc.npz')
    if exists(csr_name) and exists(csc_name):
        return True
    return False
        
def iter_np(m, row):
    for index in range(m.indptr[row], m.indptr[row+1]):
        yield m.indices[index], m.data[index]


cf = ItemBasedRecommender()
cf.load_csr_matrix(metric_type='combined')
cf.preprocess(prediction=False)
print(cf.similar_items())