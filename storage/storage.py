import shelve

from os import makedirs

from os.path import expanduser
from os.path import join
from os.path import exists

STORAGE_DIR = expanduser('~/.vk/')
PERSISTANCE_PATH = join(STORAGE_DIR, 'credentials')

class Storage:
    def folderize(f):
        def wrapper(self, *args, **kwargs):
            if not exists(STORAGE_DIR):
                makedirs(STORAGE_DIR)
            return f(self, *args, **kwargs)
        return wrapper

    @folderize
    def synchronize(f):
        def wrapper(self, *args, **kwargs):
            with shelve.open(PERSISTANCE_PATH) as shelf:
                value = f(self, shelf, *args, **kwargs)
            return value
        return wrapper

    @synchronize
    def token(self, shelf):
        return shelf['token']

    @synchronize
    def update_token(self, shelf, key):
        shelf['token'] = key

    @synchronize
    def address(self, shelf):
        return shelf['address']

    @synchronize
    def update_address(self, shelf, key):
        shelf['address'] = key
