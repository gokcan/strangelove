from strangelove.utility import similarity_base

class CosineSimilarity(similarity_base.SimilarityBase):
    """Cosine Similarity

    :type data: csr_matrix
    :param data: sparse matrix

    """

    def __init__(self, data):        
        self.data = data

    def train(self):
        """
        Produces new by using cosine similarity

        #TODO: replace with custom method to reduce dependency
        """
        self.normalize(self.data)

        from sklearn.metrics.pairwise import cosine_similarity
        # column-based cosine similarity
        return cosine_similarity(self.data.transpose(), dense_output=False)
