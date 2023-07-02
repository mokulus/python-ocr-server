import imghdr
from functools import cache
from pathlib import Path


class FileValidator:
    def __init__(self, filename):
        self.filename = filename
        self._allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        self._allowed_types = {'png', 'jpeg', 'gif'}

    @cache
    def check(self):
        if Path(self.filename).suffix[1:] not in self._allowed_extensions:
            return False
        return imghdr.what(self.filename) in self._allowed_types
