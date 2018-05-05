from strangelove.engine import base

class HybridRecommender(base.Recommender):
    """
      Hybrid Recommender for movies by using both content-based and collabrative recommendations. 

      :type disabled_metrics: list
      :param disabled_metrics: Excludes some metrics for recommendation

      :type content_rate: int
      :param content_based: Ratio for content-based recommendation. It must be less than 1, bigger than 0.
                            Default to 0.4.
    """
    def __init__(self, disabled_metrics: list=None, content_rate=0.4):
        super().__init__(disabled_metrics)
        
        assert 0 < content_rate < 1
        self.content_rate = content_rate
        self.collaborative_rate = 1 - collaborative_rate

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
        pass
    