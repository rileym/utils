import numpy as np
import os
import pandas as pd
import codecs

from itertools import imap

#
# DataFrame utils
#

def drop_columns_by_name_predicate(df, drop_predicate):
    '''Drop columns of df whose names match the drop_predicate.'''
    
    drop_columns = filter(drop_predicate, list(df.columns))
    return df.drop(labels = drop_columns, axis = 1)

def keep_columns_by_name_predicate(df, keep_predicate):
    '''Keep columns of df whose names match the keep_predicate''' 

    keep_columns = filter(keep_predicate, list(df.columns))
    return df.loc[:, keep_columns]

def partition_df(df, n_partitions):
    '''
    Partition a DataFrame 'df' into 'n_partitions' DataFrames that partition the original DataFrame.
    '''
    return np.array_split(df, n_partitions, axis = 0)

def index_to_columns(df, new_index_name = 'index'):
    '''
    Move index of DataFrame 'df' to the columns with the name given by 'new_index_name'.
    '''
    df.index.rename(new_index_name, inplace = True)
    return df.reset_index()

def vstack_dfs(dfs):
    '''
    Vertically stack DataFrame into a single DataFrame (new dataframe will have more rows).
    '''
    return pd.concat(dfs, axis = 0, ignore_index = True)

def hstack_dfs(dfs):
    '''
    Horizontally stack DataFrame into a single DataFrame (new dataframe will have more columns).
    '''
    return pd.concat(dfs, axis = 1, ignore_index = False) 

def df_select_gen(df, col_subset = None, squeeze = False):
    '''
    Generate rows from a DataFrame as tuples corresponding to columns in 'col_subset'.
    '''

    col_subset = col_subset if col_subset is not None else list(df.columns)
    if not squeeze or len(col_subset) > 1:

        for r in df.itertuples(index = False, name = "Record"):
            out = tuple(getattr(r, col_name, None) for col_name in col_subset)
            yield out

    else:
        col_name = col_subset[0]
        for r in df.itertuples(index = False, name = "Record"):
            yield getattr(r, col_name, None)


#
# Load and Persist
#

def standard_csv_update(src_csv_path, new_dfs, dest_csv_path = None):
    '''
    Add rows from DataFrames, 'new_dfs', to the DataFrame saved at 'src_csv_path', saving the updated
    csv at 'src_csv_path' unless 'dest_csv_path' is specified.
    '''

    normpath = os.path.normpath
    is_new_dest_path = ( dest_csv_path is not None ) and ( normpath(src_csv_path) != normpath(dest_csv_path) )

    if new_dfs or is_new_dest_path:

        dest_csv_path = src_csv_path if dest_csv_path is None else dest_csv_path
        df_to_update = standard_csv_load(src_csv_path)
        dfs = [df_to_update] + new_dfs
        updated_df = vstack_dfs(dfs)
        standard_csv_save(updated_df, dest_csv_path)

# def standard_chunked_csv_load(df_path, chunksize, columns = None, **kwargs):
#     '''

#     '''

#     chunks_iter = standard_csv_chunked_load_iter(
#                                     df_path, 
#                                     columns = columns, 
#                                     chunksize = chunksize, 
#                                     **kwargs
#                                    )
#     return vstack_dfs(chunks_iter)

def standard_chunked_csv_load_iter(df_path, chunksize, columns = None, **kwargs):
    '''
    Load DataFrame from csv in iterable of DataFrame chunks.
    '''
    return standard_csv_load(df_path = df_path, columns = columns, chunksize = chunksize, **kwargs)

def standard_csv_load(df_path, columns = None, encoding = u'utf8', **kwargs):
    '''
    Load a csv with standard (for my preferences) settings.
    '''
    return pd.read_csv(
        filepath_or_buffer = df_path,
        names = columns,
        encoding = encoding, 
        **kwargs
    )

def standard_csv_save(df, save_path, encoding = u'utf8', **kwargs):
    '''
    Save a DataFrame as a csv with standard (for my preferences) settings.
    '''
    df.to_csv(save_path,
                header = True,
                index = False,
                encoding = encoding,
                **kwargs
    )

def stack_load_txt_files(paths, line_parser, columns, encoding = u'utf8'):
    '''
    Load text files into a dataframe. 
    paths: paths to the text files
    line_parser: a function that takes a line from the text file and returns a tuple (row)
    columns: column names for the output dataframe.
    encoding: encoding of the text file
    '''
    
    for path in paths:
        dfs = []
        with codecs.open(path, 'rb', encoding = encoding) as f:
            df = pd.DataFrame.from_records(
                                            data = imap(line_parser, f), 
                                            columns = columns
                                           )
        dfs.append(df)    
        
    return pd.concat(dfs, axis = 0, ignore_index = True)