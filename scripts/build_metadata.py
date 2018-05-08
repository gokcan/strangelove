import argparse
import logging
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'strangelove')))
from strangelove.process.reader import Iterator, FileType
from strangelove.process.writer import Writer


"""
    Maps string fields in metadata.csv with unique ids.

        format: 'string-id'

"""

def main():
    path = os.path.abspath(
        os.path.join('../strangelove',
                     'strangelove/dataset/movielens/100k'))
    filepath = '{}/{}'.format(path, 'meta.csv')

    metadata = list(Iterator(file_type=FileType.METADATA))
    directors, cast, genres = (set() for i in range(3))
    for movie in metadata:
        if movie.director:
            directors.update(movie.director.split('|'))

        if movie.cast:
            cast.update(movie.cast.split('|'))
        
        if movie.genres:
            genres.update(movie.genres.split('|'))
    
    director_dict = {key: index for index, key in enumerate(directors)}
    cast_dict = {key: index for index, key in enumerate(cast)}
    genre_dict = {key: index for index, key in enumerate(genres)}


    writer = Writer(filepath=filepath)
    for movie in metadata:
        director, cast, genres = movie.director, movie.cast, movie.genres
        if director:
            movie_director = ['{}-{}'.format(el, director_dict[el]) for el in director.split('|')]
        if cast:
            movie_cast = ['{}-{}'.format(el, cast_dict[el]) for el in cast.split('|')]
        if genres:
            movie_genre = ['{}-{}'.format(el, genre_dict[el]) for el in genres.split('|')]

        out = {
            'movieId': movie.movieId,
            'title': movie.title,
            'releaseDate': movie.releaseDate,
            'runtime':  movie.runtime,
            'keywords': movie.keywords,
            'budget': movie.budget,
            'overview': movie.overview,
            'tagline':  movie.tagline,
            'popularity': movie.popularity,
            'revenue': movie.revenue,
            'director': '|'.join(movie_director),
            'cast': '|'.join(movie_cast),
            'genres': '|'.join(movie_genre),
        }
        
        writer.write(out)


if __name__ == '__main__':
    main()
