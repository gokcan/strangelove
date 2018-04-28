import csv
import errno
import logging
import os


logger = logging.getLogger(__name__)

_Spec = (
    'movie_id',
    'title',
    'genres',
    'overview',
    'popularity',
    'revenue',
    'vote_average',
    'vote_count',
)


class Writer(object):
    # TODO(sonmezonur): Default path
    def __init__(self, filepath: str):
        self.fieldnames = _Spec
        self.filepath = filepath
        self._file = None
        self._writer = None

    @property
    def writer(self):
        if self._writer is not None:
            return self._writer
        try:
            _ensure_path(self.filepath)
            self._file = open(self.filepath, 'w')
        except Exception as e:
            logger.error(getattr(e, 'message', e))

        self._writer = csv.DictWriter(
            self._file, fieldnames=self.fieldnames)
        # initialize header
        self._writer.writeheader()
        return self._writer

    def write(self, row: dict) -> None:
        for key, _ in row.items():
            assert key in self.fieldnames

        self.writer.writerow(row)
        self._file.flush()

    def close(self):
        if self._file is not None:
            self._file.close()


def _ensure_path(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
