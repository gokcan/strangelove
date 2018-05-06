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
    _MAX_MOVIE_ID = 9066

    def __init__(self):
        self._map = None
        self._map_origin = None

    def get_movie_id(self, id: int):
        return self._map.get(id, None)
    
    def get_id(self, id: int):
        return self._map_origin.get(id, None)

    def build_utility_csr(self):
        rate_list = list(Iterator(file_type=FileType.RATING))
        data, row, col = ([] for i in range(3))

        for rate in rate_list:
            row.append(float(rate.userId))
            data.append(float(rate.rating))
            col.append(float(rate.movieId))

        col = self._map_movie_ids(col)

        csr = csr_matrix((data, (row, col)), shape=(self._MAX_USER_ID, self._MAX_MOVIE_ID))
        csr.eliminate_zeros()
        csc = csr.tocsc()

        print(csr.toarray()[1][self.get_id(31)])  # prints rating 2.5
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
        csc = csr.tocsc()
        np.savez("norm-matrix-csr", data=csr.data,
                 indices=csr.indices, indptr=csr.indptr, shape=csr.shape)
        np.savez('norm-matrix-csc', data=csc.data,
                 indices=csc.indices, indptr=csc.indptr, shape=csc.shape)


    def _map_movie_ids(self, col):
        """Maps movie ids to incremental numeric ids"""
        map_csr = []

        set_csr = set(col)
        for index, movie_id in enumerate(set_csr):
            map_csr.append((int(movie_id), index))

        # cache ids into map
        self._map =  dict((v, k) for k, v in map_csr)
        self._map_origin = dict(map_csr)
        return [float(self._map_origin[id]) for id in col]


util = MatrixUtility()
util.build_utility_csr()
util.normalize()