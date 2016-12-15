import shutil
import re
import os
from functools import partial
from itertools import imap
import tempfile
import cloudpickle as pkl

#
# File/Folder Utils
#

def normjoin(*args):
    '''Build and return the normalized filepath from the series of segments in ``args``.'''
    return os.path.normpath(os.path.join(*args))

def listpaths(dir_):
    '''List full paths of all files in the directory ``dir_``.'''

    dir_ = os.path.normpath(dir_)
    filenames = os.listdir(dir_)
    repath = lambda filename: normjoin(dir_, filename)
    return map(repath, filenames)

def directory_filename_inventory(dir_, basename_pred = None):
    '''
    Returns the basenames of the files in the directory matching ``basename_pred`` predicate. 
    
    If ``basename_pred`` is not given, all file basenames are returned.
    '''

    dir_inventory = os.listdir(dir_)
    paths = map(lambda bn: normjoin(dir_, bn), dir_inventory)
    filepaths = filter(os.path.isfile, paths)
    filenames = map(os.path.basename, filepaths)
    filenames_meeting_pred = filter(basename_pred, filenames)
    return filenames_meeting_pred

def filepaths_matching_re(dir_, re_ptrn):
    '''Return the full filepaths in directory ``dir_`` whose filenames match the regular expression ``re_ptrn``.'''
    match_pred = partial(re.match, re_ptrn)
    matching_filenames = directory_filename_inventory(dir_, match_pred)
    repath = lambda filename: normjoin(dir_, filename)
    return map(repath, matching_filenames)

def dir_is_empty(dir_):
    '''Check that ``dir_`` is an empty directory.'''
    return not bool(os.listdir(dir_))

def dir_exists(dir_):
    '''Check that ``dir_`` exists.'''
    return os.path.isdir(dir_)

def dir_does_not_exist(dir_):
    '''Check that directory ``dir_`` does not exists.'''
    return not os.path.exists(dir_)

def remove_file(filepath):
    '''Remove file at ``filepath``.'''
    os.remove(filepath)

def remove_dir(dir_):
    '''Remove a directory ``dir_``.'''
    shutil.rmtree(dir_)

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

# TODO: Change error types raised
class TempDir(object):
    ''' Convience class to create, populate, and close a temporary file.'''

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def open(self):
        self._dir = tempfile.mkdtemp()

    def close(self):
        remove_dir(self._dir)

    def is_open(self):
        try:
            return dir_exists(self._dir)
        except AttributeError:
            return False

    def __len__(self):
        try:
            return len(listpaths(self._dir))
        except OSError:
            raise OSError('Size of {class_} not defined for a closed {class_}.'.format(class_ = self.__class__.__name__))

    @property
    def dir_(self):
        if self.is_open():
            return self._dir
        else:
            raise AttributeError('TempDir is currently closed.')

    def _make_path_form_filename(self, filename):
        return normjoin(self._dir, filename)

    def next_path(self):
        candidate_filename = next(tempfile._get_candidate_names())
        return self._make_path_form_filename(candidate_filename)

    def iter_candidate_paths(self):
        return imap(self._make_path_form_filename, tempfile._get_candidate_names())

    def iter_paths(self):
        return listpaths(self._dir)

# object persist

def load_pkl(path):
    '''Load a (cloud)pickled object at ``path``.'''
    with open(path, 'rb') as f:
        return pkl.load(f)
    
def dump_pkl(obj, path):
    '''Persist object ``obj`` to ``path`` with (cloud)pickle.'''
    with open(path, 'wb') as f:
        pkl.dump(obj, f)

def load_json(path):
    '''Load a json object into a dictinoary.'''
    with open(path, 'rb') as f:
        return json.load(f)


