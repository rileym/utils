import sys
sys.path.append('..')

import numpy as np
import constants as CNST
import os
import pandas as pd
import codecs

from itertools import imap

#
# DataFrame utils
#

def partition_df(df, n_partitions):
    return np.array_split(df, n_partitions, axis = 0)

def index_to_columns(df, new_index_name = 'index'):
    df.index.rename(new_index_name, inplace = True)
    return df.reset_index()

def vstack_dfs(dfs):
    return pd.concat(dfs, axis = 0, ignore_index = True)

def hstack_dfs(dfs):
    return pd.concat(dfs, axis = 1, ignore_index = False) 

def df_select_gen(df, col_subset = None, squeeze = False):

    col_subset = col_subset if col_subset is not None else list(df.columns)
    if not squeeze or len(col_subset) > 1:

        for r in df.itertuples(index = False, name = "Record"):
            out = tuple(getattr(r, col_name, None) for col_name in col_subset)
            yield out

    else:
        col_name = col_subset[0]
        for r in df.itertuples(index = False, name = "Record"):
            yield getattr(r, col_name, None)

def stack_load_txt_files(paths, line_parser, columns):
    
    for path in paths:
        dfs = []
        with codecs.open(path, 'rb', encoding = CNST.ENCODING) as f:
            df = pd.DataFrame.from_records(
                                            data = imap(line_parser, f), 
                                            columns = columns
                                           )
        dfs.append(df)    
        
    return pd.concat(dfs, axis = 0, ignore_index = True)

#
# CSV load
#

def update_standard_csv(src_csv_path, new_dfs, dest_csv_path = None):

    normpath = os.path.normpath
    is_new_dest_path = ( dest_csv_path is not None ) and ( normpath(src_csv_path) != normpath(dest_csv_path) )

    if new_dfs or is_new_dest_path:

        dest_csv_path = src_csv_path if dest_csv_path is None else dest_csv_path
        df_to_update = standard_csv_load(src_csv_path)
        dfs = [df_to_update] + new_dfs
        updated_df = vstack_dfs(dfs)
        standard_csv_save(updated_df, dest_csv_path)

def chunked_csv_load(df_path, columns = None, chunksize = CNST.DF_CHUNK_SIZE, **kwargs):

    chunks_iter = standard_csv_load(
                                    df_path, 
                                    columns = columns, 
                                    chunksize = chunksize, 
                                    **kwargs
                                   )
    return pd.concat(chunks_iter, axis = 0, ignore_index = True)

def standard_csv_chunked_load(df_path, columns = None, chunksize = CNST.SENTENCE_CHUNK_SIZE, **kwargs):
    return standard_csv_load(df_path = df_path, columns = columns, chunksize = chunksize, **kwargs)

def standard_csv_load(df_path, columns = None, **kwargs):
    return pd.read_csv(
        filepath_or_buffer = df_path,
        names = columns,
        encoding = CNST.ENCODING, 
        **kwargs
    )

def standard_csv_save(df, save_path, **kwargs):
    df.to_csv(save_path,
                header = True,
                index = False,
                encoding = CNST.ENCODING,
                **kwargs
    )

def alt_encoding_csv_load(df_path, encoding, columns = None, **kwargs):

    return pd.read_csv(
        filepath_or_buffer = df_path,
        encoding = encoding,
        names = columns, 
        **kwargs
    )