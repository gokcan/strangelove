import codecs
import csv
import logging
from collections import namedtuple

import strangelove

logger = logging.getLogger(__name__)


class FileType(object):
    MOVIE = 0
    RATING = 1
    LINK = 2
    TAG = 3

    _VALUES_TO_NAMES = {
        0: 'MOVIE',
        1: 'RATING',
        2: 'LINK',
        3: 'TAG',
    }

    _NAMES_TO_VALUES = {
        'MOVIE': 0,
        'USER': 1,
        'LINK': 2,
        'TAG': 3,
    }

    """ Immutable Representation of data collected from csv files. """
    _VALUES_TO_TUPPLE = {
        0: namedtuple('Movie', ('movieId', 'title', 'genres')),
        1: namedtuple('Rating', ('userId', 'movieId', 'rating', 'timestamp')),
        2: namedtuple('Link', ('movieId', 'imdbId', 'tmdbId')),
        3: namedtuple('Tag', ('userId', 'movieId', 'tag', 'timestamp')),
    }

    _VALUES_TO_PATH = {
        0: '{}/movies.csv'.format(strangelove.STATIC_ROOT),
        1: '{}/ratings.csv'.format(strangelove.STATIC_ROOT),
        2: '{}/links.csv'.format(strangelove.STATIC_ROOT),
        3: '{}/tags.csv'.format(strangelove.STATIC_ROOT),
    }


class BaseIterator(object):
    def __init__(self, file_type=FileType.MOVIE, encoding=None):
        self._reader = None
        self._file = None
        self.encoding = encoding
        self.filepath = FileType._VALUES_TO_PATH[file_type]
        self.parser = Parser(file_type=file_type)

    @property
    def reader(self):
        if self._reader is not None:
            return self._reader

        try:
            self._file = open(self.filepath)
        except Exception as e:
            logger.error(getattr(e, 'message', e))

        if self.encoding is not None:
            self.file = codecs.encode(self.file, encoding=self.encoding)

        self._reader = csv.reader(self._file)
        next(self._reader)
        return self._reader

    def __iter__(self):
        return self

    def __next__(self) -> namedtuple:
        pass

    def __close__(self):
        if self._file is not None:
            self._file.close()


class Iterator(BaseIterator):
    """Base Iterator to effectively parse csv files.

    Example:
        for el in Iterator(file_type=FileType.MOVIE):
            do_smth()

        - Sync Parse
        for el1, el2 in zip(Iterator(), Iterator(FileType.LINK)):
            do_smth()

    """
    def __init__(self, file_type=FileType.MOVIE, encoding=None):
        super().__init__(file_type, encoding)

    def __next__(self) -> namedtuple:
        return self.parser.parse(next(self.reader))


class Parser(object):
    def __init__(self, file_type: int):
        self.tuple = FileType._VALUES_TO_TUPPLE[file_type]

    def parse(self, line) -> namedtuple:
        return self.tuple(*line)
