import argparse
import logging
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'strangelove')))
from strangelove.process.reader import Iterator, FileType
from strangelove.process.fetch import Movie as MovieFetcher
from strangelove.process.writer import Writer

"""
    usage: build_csv.py [-h] --file FILE [--path PATH]

    optional arguments:
        --file FILE, -f FILE
        --path PATH, -p PATH

"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True)
    parser.add_argument('--path', '-p', type=str, default=None)
    args = parser.parse_args()

    if args.path is None:
        args.path = os.path.abspath(
            os.path.join('../strangelove',
                         'strangelove/dataset/movielens/100k/out'))

    filepath = '{}/{}'.format(args.path, args.file)

    fetcher = MovieFetcher()
    writer = Writer(filepath=filepath)
    for movie, link in zip(Iterator(), Iterator(file_type=FileType.LINK)):
        res = fetcher.fetch(link.tmdbId)
        out = {
            'movie_id': movie.movieId,
            'title': movie.title,
            'genres': movie.genres,
            'overview': res.get('overview', ''),
            'popularity': res.get('popularity', ''),
            'revenue': res.get('revenue', ''),
            'vote_average': res.get('vote_average', ''),
            'vote_count': res.get('vote_count', '')
        }

        writer.write(out)


if __name__ == '__main__':
    main()
