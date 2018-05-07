
class Recommender(object):
    """
      Base Recommender for movies. 
    """
    def __init__(self):
        pass
    
    def load_csv(self, matrix: str):
        """Preprocess part of recommendation.
        :type matrix: str
        :param matrix: npz file

        """
        pass

    
    def preprocess(self):
        """Preprocess part of recommendation.
        :type matrix: str
        :param matrix: npz file

        """
        pass

    def recommend(self, id: int, size: int=10) -> list:
        """Recommends movie.
        :type id: int
        :param id: user/movie id according to the recommender type

        :type size: int
        :param size: 

        """
        pass
