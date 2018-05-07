import numpy as np
from scipy.sparse import coo_matrix
from strangelove.utility import similarity_base

class TFIDFSimilarity(similarity_base.SimilarityBase):
    """TFIDF Similarity

    :type data: csr_matrix
    :param data: sparse matrix

    """
    def __init__(self, data):        
        self.data = data

    def train(self):
        matrix = coo_matrix(self.data)
        
        # calculate IDF
        N = float(matrix.shape[0])
        idf = np.log(N) - np.log1p()
        
        matrix.data = np.sqrt(matrix.data) * idf[matrix.col]
        return self.normalize(matrix)
