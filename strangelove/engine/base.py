
class Recommender(object):
    """
      Base Recommender for movies. 

      :type disabled_metrics: list
      :param disabled_metrics: Excludes some metrics for recommendation
    """
    def __init__(self, disabled_metrics: list=None):
        self.disabled = disabled_metrics

    def recommend(self, id: int, size: int=10) -> list:
        """Recommends movie.
        :type id: int
        :param id: user/movie id according to the recommender type

        :type size: int
        :param size: 

        """
        pass
    
    # TODO
    def export(self, type='txt') -> None:
        """ Exports recommendations to the file.
        :type type: str
        :param type: type of file{csv, txt, sqlite, etc.}

        """

        pass 