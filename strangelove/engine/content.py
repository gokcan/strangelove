from strangelove.engine import base

class ContentRecommender(base.Recommender):
    """
      Content-Based Recommender for movies. 

      :type disabled_metrics: list
      :param disabled_metrics: Excludes some metrics for recommendation

    """
    def __init__(self, disabled_metrics: list=None):
        super().__init__(disabled_metrics)

    def recommend(self, movie_id: int, size: int=10) -> list:
        """Recommends movie.
        :type id: int
        :param id: user id according to the recommender type

        :type size: int
        :param size: 

        """
        pass