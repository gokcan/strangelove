import logging
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, csc_matrix
from strangelove.process.reader import Iterator, FileType
from strangelove import STATIC_ROOT

logger = logging.getLogger(__name__)


class MatrixUtility(object):
    """ Builder """
    _MAX_USER_ID = 672
    _MAX_MOVIE_ID = 163950

    def __init__(self):
        pass

    def build_utility_csr(self):
        rate_list = list(Iterator(file_type=FileType.RATING))
        data, row, col = ([] for i in range(3))

        for rate in rate_list:
            row.append(float(rate.userId))
            col.append(float(rate.movieId))
            data.append(float(rate.rating))

        csr = csr_matrix((data, (row, col)), shape=(self._MAX_USER_ID, self._MAX_MOVIE_ID))
        csr.eliminate_zeros()
        csc = csr.tocsc()

        print(csr.toarray()[1][31])  # prints rating 2.5
        np.savez('matrix-csr', data=csr.data, indices=csr.indices,
                 indptr=csr.indptr, shape=csr.shape)
        np.savez('matrix-csc', data=csc.data, indices=csc.indices,
                 indptr=csc.indptr, shape=csc.shape)

    def normalize(self, matrix='matrix-csr.npz'):
        npz = np.load(matrix)
        csr = csr_matrix((npz["data"], npz["indices"],
                                  npz["indptr"]), shape=npz["shape"])

        total_users = self._MAX_USER_ID

        for ind in range(1, total_users):
            ratings = csr[ind]
            if ratings.data.size:
                csr.data[csr.indptr[ind]:csr.indptr[ind+1]] -= int(np.mean(ratings.data))

        csr.eliminate_zeros()
        #print(utility_csr.toarray()[1][31])
        csc = csr.tocsc()
        np.savez("norm-matrix-csr", data=csr.data,
                 indices=csr.indices, indptr=csr.indptr, shape=csr.shape)
        np.savez('norm-matrix-csc', data=csc.data,
                 indices=csc.indices, indptr=csc.indptr, shape=csc.shape)


util = MatrixUtility()
util.build_utility_csr()
util.normalize()
