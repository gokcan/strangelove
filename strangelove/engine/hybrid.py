from strangelove.engine import base

class HybridRecommender(base.Recommender):
    """
      Hybrid Recommender for movies by using collabrative recommendations. 

      :type disabled_metrics: list
      :param disabled_metrics: Excludes some metrics for recommendation

    """
    def __init__(self, disabled_metrics: list=None):
        super().__init__(disabled_metrics)
   
    def preprocess(self, matrix: str):
        """Preprocess part of recommendation.
        :type matrix: str
        :param matrix: npz file

        """
        raise Exception("Not Implemented")     

    def recommend(self, user_id: int, movie_id: int, size: int=10) -> list:
          """Recommends movie.
        :type user_id: int
        :param id: ID of user.
        
        :type movie_id: int
        :param id: Id of movie.

        :type size: int
        :param size: Size of list to return

        returns lists of recommended movies.

        """
        raise Exception("Not Implemented")     
