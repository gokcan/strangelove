from scipy.sparse import coo_matrix
from numpy import bincount, sqrt

class SimilarityBase(object):
    """
        Base Similarity
    """

    def train(self):
        pass

    def normalize(self, X):
        X = coo_matrix(X)
        X.data = X.data / sqrt(bincount(X.row, X.data ** 2))[X.row]
        return X
