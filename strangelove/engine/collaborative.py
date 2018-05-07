from strangelove.engine import base
import strangelove.process.reader
from strangelove.process.util import MatrixUtility
from strangelove.utility.cosine_similarity import CosineSimilarity
from strangelove.utility.tfidf_similarity import TFIDFSimilarity
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
        self.csr = None
        self.similary_matrix = None

    def load_csr_matrix(self,  matrix: str='matrix-csr.npz'):
        "Loads sparse csv"
        self.utility.build_utility_csr()

        npz = np.load(matrix)
        self.csr = csr_matrix((npz["data"], npz["indices"],
                                    npz["indptr"]), shape=npz["shape"])

    def similar_items(self, item_id=1029, size=10):
        if size >= self.similarity_matrix.shape[0]:
            return []
        return sorted(
            list(iter_np(self.similarity_matrix, item_id)), key=lambda x: -x[1])[:size]
    
    def preprocess(self, model_name='cosine'):
        """Trains the dataset and creates similarity matrix according to similarity model.
        :type model_name: str
        :param model_name: Applied model name.
        """
        if model_name == 'cosine':
            model = CosineSimilarity(self.csr)
        elif model_name == 'svd':
            model = MatrixFactorization(self.csr)
        elif model_name == 'tfidf':
            model = TFIDFSimilarity(self.csr)
        else:
            raise Exception("Unsupported similarity model")
        
        # builds similarity matrix based on similarity model
        similarity = model.train()
        self.similarity_matrix = csr_matrix(similarity)

    def recommend(self, user_id, size: int=10, similarity_constraint=0.6) -> list:
        """Recommends movie.
        :type user_id: int
        :param id: ID of user.

        :type size: int
        :param size: Size of list to return

        returns lists of recommended movies.
        """
        pass

        
def iter_np(m, row):
    for index in range(m.indptr[row], m.indptr[row+1]):
        yield m.indices[index], m.data[index]


cf = ItemBasedRecommender()
cf.load_csr_matrix()
cf.preprocess()
print(cf.similar_items())
cf.preprocess(model_name='tfidf')
print(cf.similar_items())