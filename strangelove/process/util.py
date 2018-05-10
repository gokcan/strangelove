import logging
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, csc_matrix
from strangelove.process.reader import Iterator, FileType
from strangelove import STATIC_ROOT
from strangelove.process.mapper import Mapper
from os.path import exists

logger = logging.getLogger(__name__)


class MatrixUtility(object):
    """ Builder """
    _MAX_USER_ID = 672
    _MAX_MOVIE_ID = 164980
    _MAX_DIRECTOR_ID = 3978
    _MAX_CAST_ID = 16838
    _MAX_GENRE_ID = 20

    def __init__(self):
        pass

    def build_user_rating_csr(self):
        rate_list = list(Iterator(file_type=FileType.RATING))
        data, row, col = ([] for i in range(3))

        for rate in rate_list:
            row.append(float(rate.userId))
            data.append(float(rate.rating))
            col.append(float(rate.movieId))

        csr = csr_matrix((data, (row, col)), shape=(self._MAX_USER_ID, self._MAX_MOVIE_ID))
        _save_csr_matrix(csr=csr, field_type='rating')
    
    def build_movie_profile_csr(self):
        metadata = list(Iterator(file_type=FileType.META))

        row, col, data = _extract_director_info(metadata)
        csr = csr_matrix((data, (row, col)), shape=(self._MAX_MOVIE_ID, self._MAX_DIRECTOR_ID))
        _save_csr_matrix(csr=csr, field_type='director')
    
        row, col, data = _extract_genre_info(metadata)
        csr = csr_matrix((data, (row, col)), shape=(self._MAX_MOVIE_ID, self._MAX_GENRE_ID))
        _save_csr_matrix(csr=csr, field_type='genre')

        row, col, data = _extract_cast_info(metadata)
        csr = csr_matrix((data, (row, col)), shape=(self._MAX_MOVIE_ID, self._MAX_CAST_ID))
        _save_csr_matrix(csr=csr, field_type='cast')


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
    

    def build_user_tag_csr(self):
        from difflib import SequenceMatcher

        tag_list = list(Iterator(file_type=FileType.TAG))
        keyword_list = "".join(list(tag.tag for tag in tag_list))
        similarities, row, col = (list() for i in range(3))
        for tag_dict in tag_list:
            similarity_ratio =  SequenceMatcher(None, keyword_list, tag_dict.tag).ratio()
            similarities.append(similarity_ratio)
            row.append(float(tag_dict.userId))
            col.append(float(tag_dict.movieId))
        csr = csr_matrix((similarities, (row, col)), shape=(self._MAX_USER_ID, self._MAX_MOVIE_ID))
        _save_csr_matrix(csr=csr, field_type='tag')



def _save_csr_matrix(field_type, csr):
    csr_name = '{}{}'.format(field_type, '-csr')
    csc_name = '{}{}'.format(field_type, '-csc')

    csr.eliminate_zeros()
    csc = csr.tocsc()

    np.savez(csr_name, data=csr.data,
            indices=csr.indices, indptr=csr.indptr, shape=csr.shape)
    np.savez(csc_name, data=csc.data,
            indices=csc.indices, indptr=csc.indptr, shape=csc.shape)   

def _extract_director_info(metadata):
    data, row, col = ([] for i in range(3))
    for movie in metadata:
        if movie.director:
            for director in movie.director.split('|'):
                assert len(director.split('&')) == 2
                row.append(int(movie.movieId))
                col.append(int(director.split('&')[1]))
                data.append(1)
    return row, col, data

def _extract_genre_info(metadata):
    data, row, col = ([] for i in range(3))
    for movie in metadata:
        if movie.genres:
            for genre in movie.genres.split('|'):
                assert len(genre.split('&')) == 2
                row.append(int(movie.movieId))
                col.append(int(genre.split('&')[1]))
                data.append(1)
    return row, col, data    

def _extract_cast_info(metadata):
    data, row, col = ([] for i in range(3))
    for movie in metadata:
        if movie.cast:
            for cast in movie.cast.split('|'):
                assert len(cast.split('&')) == 2
                row.append(int(movie.movieId))
                col.append(int(cast.split('&')[1]))
                data.append(1)
    return row, col, data


util = MatrixUtility()

