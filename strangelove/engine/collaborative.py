from strangelove.engine import base
from strangelove.process.reader import Iterator, FileType

class CollaborativeRecommender(base.Recommender):
    """
      Collabrative Recommender for movies. 

      :type disabled_metrics: list
      :param disabled_metrics: Excludes some metrics for recommendation
    """
    def __init__(self, disabled_metrics: list=None):
        super().__init__(disabled_metrics)

    def recommend(self, user_id: int, size: int=10) -> list:
        """Recommends movie.
        :type user_id: int
        :param id: ID of user.

        :type size: int
        :param size: Size of list to return

        returns lists of recommended movies.
        """
        pass