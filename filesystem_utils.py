import shutil
import re
import os

from functools import partial
import cloudpickle as pkl

#
# File/Folder Utils
#

def normjoin(*args):
    return os.path.normpath(os.path.join(*args))

def listpaths(dir_):

    dir_ = os.path.normpath(dir_)
    filenames = os.listdir(dir_)
    repath = lambda filename: normjoin(dir_, filename)
    return map(repath, filenames)

def directory_filename_inventory(dir_, basename_pred = None):

        dir_inventory = os.listdir(dir_)
        paths = map(lambda bn: normjoin(dir_, bn), dir_inventory)
        filepaths = filter(os.path.isfile, paths)
        filenames = map(os.path.basename, filepaths)
        filenames_meeting_pred = filter(basename_pred, filenames)
        return filenames_meeting_pred       

def filepaths_matching_re(dir_, re_ptrn):

    match_pred = partial(re.match, re_ptrn)
    return directory_filename_inventory(dir_, re_ptrn)

def dir_is_empty(dir_):
    return not bool(os.listdir(dir_))

def dir_exists(dir_):
    return os.path.isdir(dir_)

def dir_does_not_exist(dir_):
    return not os.path.exists(dir_)

def remove_file(filepath):
    os.remove(filepath)

def remove_dir(dir_):
    shutil.rmtree(dir_)

# object persist

def load_pkl(path):
    with open(path, 'rb') as f:
        return pkl.load(f)
    
def dump_pkl(obj, path):
    with open(path, 'wb') as f:
        pkl.dump(obj, f)
