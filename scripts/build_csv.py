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
        director, cast, keywords = ([] for i in range(3))

        if 'status_code' in res:
            value = res['status_code']
            print("Status Code: {}, Movie ID: {}".format(value,link.movieId))

        else:  # status_code is not set for successful read operations.
            if 'credits' in res:
                credits = res['credits']

                for person in credits['crew']:
                    if person['job'] == 'Director':
                        director.append(person['name'])

                for person in credits['cast']:
                    if person['order'] < 5:
                        cast.append(person['name'])

            for keyword in res['keywords']['keywords']:
                keywords.append(keyword['name'])
            
            out = {
                'movieId': movie.movieId,
                'title': movie.title,
                'genres': movie.genres,
                'releaseDate': res.get('release_date', ''),
                'runtime': res.get('runtime', ''),
                'budget': res.get('budget', ''),
                'overview': res.get('overview', ''),
                'tagline': res.get('tagline', ''),
                'popularity': res.get('popularity', ''),
                'revenue': res.get('revenue', ''),
                'director': '|'.join(director),
                'cast': '|'.join(cast),
                'keywords': '|'.join(keywords),
            }

            writer.write(out)


if __name__ == '__main__':
    main()
