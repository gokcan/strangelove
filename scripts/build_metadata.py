import argparse
import logging
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'strangelove')))
from strangelove.process.reader import Iterator, FileType
from strangelove.process.writer import Writer

from nltk.stem.snowball import SnowballStemmer


"""
    Maps string fields in metadata.csv with unique ids.

        format: 'string-id'

    Creates mapping csv files for movie fields

"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', '-p', type=str, default='100K')
    args = parser.parse_args()
    if args.size not in ['100K', '1M']:
        raise Exception('Unsuported dataset')
  
    path = os.path.abspath(
        os.path.join('../strangelove',
                     'strangelove/dataset/movielens/{}'.format(args.size)))
    
    stemmer = SnowballStemmer(language='english')

    metadata = list(Iterator(file_type=FileType.METADATA))
    directors, cast, genres, keywords = (set() for i in range(4))
    for movie in metadata:
        if movie.director:
            directors.update(movie.director.split('|'))

        if movie.cast:
            cast.update(movie.cast.split('|')[:3])
                
        if movie.keywords:
            keyword_list = movie.keywords.split('|')
            x = []
            for k in keyword_list:
                x.append(stemmer.stem(k))
                 
            keywords.update(x)

        if movie.genres:
            if movie.genres == '(no genres listed)':
                continue
            genres.update(movie.genres.split('|'))
            

    fieldnames = ('name', 'id')
    filepath = '{}/{}'.format(path, 'director.csv')
    writer = Writer(filepath=filepath, fieldnames=fieldnames)
    director_dict = dict()
    for index, key in enumerate(directors):
        director_dict[key] = index
        writer.write({
            'name': key,
            'id': index,
        })


    filepath = '{}/{}'.format(path, 'cast.csv')
    writer = Writer(filepath=filepath, fieldnames=('name', 'id'))
    cast_dict = dict()
    for index, key in enumerate(cast):
        cast_dict[key] = index
        writer.write({
            'name': key,
            'id': index,
        })

    filepath = '{}/{}'.format(path, 'genre.csv')
    writer = Writer(filepath=filepath, fieldnames=('name', 'id'))
    genre_dict = dict()
    for index, key in enumerate(genres):
        genre_dict[key] = index
        writer.write({
            'name': key,
            'id': index,
        })

    filepath = '{}/{}'.format(path, 'keyword.csv')
    writer = Writer(filepath=filepath, fieldnames=('name', 'id'))
    keyword_dict = dict()
    for index, key in enumerate(keywords):
        keyword_dict[key] = index
        writer.write({
            'name': key,
            'id': index,
        })


    filepath = '{}/{}'.format(path, 'meta.csv')
    writer = Writer(filepath=filepath)
    for movie in metadata:
        director, cast, genres, keyword = movie.director, movie.cast, movie.genres, movie.keywords
        if director:
            movie_director = ['{}&{}'.format(el, director_dict[el]) for el in director.split('|')]
        if cast:
            movie_cast = ['{}&{}'.format(el, cast_dict[el]) for el in cast.split('|')[:3]]
        if genres:
            movie_genre = ['{}&{}'.format(el, genre_dict[el]) for el in genres.split('|')] \
                        if genres != '(no genres listed)' else []
        if keyword:
            keyword_list = keyword.split('|')
            x = []
            for k in keyword_list:
                x.append(stemmer.stem(k))
            movie_keyword = ['{}&{}'.format(el, keyword_dict[el]) for el in x]

        out = {
            'movieId': movie.movieId,
            'title': movie.title,
            'releaseDate': movie.releaseDate,
            'runtime':  movie.runtime,
            'keywords': '|'.join(movie_keyword),
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
