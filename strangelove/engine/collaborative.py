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
    def pearsonSimilarity(ratings, x, y ):
        #save movies that both users have been rated
        movieDict={}
        for movie in ratings[x]:
            if movie in ratings[y]:
                movieDict[movie] = 1
                N = len(movieDict)
        #could not find pair, then return
        if N == 0:
            return -1
        # sum of scores
        Ex = sum([ratings[x][movie] for movie in movieDict])
        Ey = sum([ratings[y][movie] for movie in movieDict])
        # sum of squared scores
        Ex2 = sum([pow(ratings[x][movie],2) for movie in movieDict])
        Ey2 = sum([pow(ratings[y][movie],2) for movie in movieDict])
        #sum of the products of paired scores
        Exy = sum([ratings[x][movie] * ratings[y][movie] for movie in movieDict])
        #pearson formula =
        numerator = (N*Exy - Ex*Ey)
        denom1 = Ex2 - pow(Ex,2)/N
        denom2 = Ey2 - pow(Ey,2)/N
        denominator = sqrt(denom1 * denom2)
        if denominator == 0: return -2 #divide by zero exception since not sure if it automatically gives error
        r = numerator / denominator
        return r
