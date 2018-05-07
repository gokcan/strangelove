import numpy as np

class MatrixFactorization(object):
    """Matrix factorization using Stochastic Gradient Descent. 

    :type ratings: np.ndarray
    :param ratings: np array for user rates


    :type number_latent_dimensions: int
    :param number_latent_dimensions: Number of latent factors for factorization model.

    :type alpha: float
    :param alpha: Learning rate of item/user factors

    :type beta: float
    :param beta: Regularization term of item/user factors

    :type size: int
    :param size: Number of iterations for calculation.
    """

    def __init__(
        self,
        ratings: np.ndarray,
        number_latent_dimensions=100,
        alpha=0.1,
        beta=0.01,
        size=20):
        assert isinstance(ratings, np.ndarray)
        
        self.ratings = ratings
        self.num_users, self.num_items = ratings.shape
        self.number_latent_dimensions = number_latent_dimensions
        self.alpha = alpha
        self.beta = beta
        self.size = size

    def train(self):
        """
        Produces a prediction based on SGD. 

        returns (full_matrix: np.ndarray, item_factors: np.ndarray, user_factors: np.ndarray)

        example:
            mf = MatrixFactorization(R, number_latent_dimensions=100, alpha=0.1, beta=0.04, size=20)
            matrix, item_factors, user_factors = mf.train()

        """
        # randomly initialize user and item factors
        self.user_factors = np.random.normal(0, .1, size=(self.num_users, self.number_latent_dimensions))
        self.item_factors = np.random.normal(0, .1, size=(self.num_items, self.number_latent_dimensions))

        # initialize the biases
        self.user_bias = np.zeros(self.num_users)
        self.item_bias = np.zeros(self.num_items)
        self.global_bias = np.mean(self.ratings[np.where(self.ratings != 0)])

        # Create a list of training samples
        samples = [
            (i, j, self.ratings[i, j])
            for i in range(self.num_users)
            for j in range(self.num_items)
            if self.ratings[i, j] > 0
        ]            

        # stochastic gradient descent for number of iterations
        for _ in range(self.size):
            np.random.shuffle(samples)
            self._sgd(samples)

        return self.full_matrix()

    def _predict_item(self, i, j) -> float:
        prediction = self.global_bias + self.user_bias[i] + self.item_bias[j]
        prediction += self.user_factors[i, :].dot(self.item_factors[j, :].T)
        return prediction

    def _sgd(self, samples) -> None:
        for i, j, val in samples:
            prediction = self._predict_item(i, j)
            err = val - prediction
            
            if err < 0.001:
                break
            
            self.user_bias[i] += self.alpha * \
                    (err - self.beta * self.user_bias[i])
            self.item_bias[j] += self.alpha * \
                    (err - self.beta * self.item_bias[j])

            # estimate rating of user for the item
            self.user_factors[i, :] += self.alpha * \
                                        (err * self.item_factors[j, :] - \
                                        self.beta * self.user_factors[i, :])
            self.item_factors[j, :] += self.alpha * \
                                        (err * self.user_factors[i, :] - \
                                        self.beta * self.item_factors[j, :])


    def full_matrix(self) -> np.ndarray:
        """
        Find the full matrix using the resultant biases, user factors and item factor
        """
        return self.global_bias + self.user_bias[:,np.newaxis] + \
                self.item_bias[np.newaxis:,] + self.user_factors.dot(self.item_factors.T)
