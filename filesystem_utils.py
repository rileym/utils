import shutil
import re
import os
from functools import partial
import cloudpickle as pkl

#
# File/Folder Utils
#

def normjoin(*args):
    '''
    Return a the combined and normalized pieces of a filepath from 'args'.
    '''
    return os.path.normpath(os.path.join(*args))

def listpaths(dir_):
    '''
    List full paths of all files in the directory 'dir_'.
    '''

    dir_ = os.path.normpath(dir_)
    filenames = os.listdir(dir_)
    repath = lambda filename: normjoin(dir_, filename)
    return map(repath, filenames)

def directory_filename_inventory(dir_, basename_pred = None):
    '''
    Returns the basenames of the files in the directory matching 'basename_pred' predicate. 
    If 'basename_pred' is not given, all basenames are returned.
    '''

    dir_inventory = os.listdir(dir_)
    paths = map(lambda bn: normjoin(dir_, bn), dir_inventory)
    filepaths = filter(os.path.isfile, paths)
    filenames = map(os.path.basename, filepaths)
    filenames_meeting_pred = filter(basename_pred, filenames)
    return filenames_meeting_pred       

def filepaths_matching_re(dir_, re_ptrn):
    '''
    Return the full filepaths in directory 'dir_' whose filenames the regular expression 're_ptrn'.
    '''
    match_pred = partial(re.match, re_ptrn)
    return directory_filename_inventory(dir_, match_pred)

def dir_is_empty(dir_):
    '''
    Check that 'dir_' is an empty directory.
    '''
    return not bool(os.listdir(dir_))

def dir_exists(dir_):
    '''
    Check that 'dir_' exists.
    '''
    return os.path.isdir(dir_)

def dir_does_not_exist(dir_):
    '''
    Check that directory 'dir_' does not exists.
    '''
    return not os.path.exists(dir_)

def remove_file(filepath):
    '''
    Remove file at 'filepath'.
    '''
    os.remove(filepath)

def remove_dir(dir_):
    '''
    Remove a directory 'dir_'.
    '''
    shutil.rmtree(dir_)

# object persist

def load_pkl(path):
    '''
    Load a (cloud)pickled object.
    '''
    with open(path, 'rb') as f:
        return pkl.load(f)
    
def dump_pkl(obj, path):
    '''
    Persist an object to 'path' with (cloud)pickle.
    '''
    with open(path, 'wb') as f:
        pkl.dump(obj, f)

def load_json(path):
    '''
    Load a json object into a dictinoary.
    '''
    with open(path, 'rb') as f:
        return json.load(f)

