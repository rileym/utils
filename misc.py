import re
import unittest
import json
import datetime
import toolz
from operator import methodcaller


#
# MOVE TO RELEVANT DOMAIN
#

def transform_date(input_date_fmt, output_date_fmt, date_raw_str):
    '''
    Transform a date string from one date formate to another.
    '''
    date = datetime.datetime.strptime(date_raw_str, input_date_fmt)
    return date.strftime(output_date_fmt)


def format_df_for_review(df, id_columns, text_column, label_column, rank_column = None, default_label = u''):

    df = df.copy()
    
    out_columns = id_columns + [text_column] + [label_column]
    
    if rank_column:
        df = df.sort_values(rank_column, ascending = False)
        out_columns.insert(len(id_columns), rank_column)
    
    df[label_column] = unicode(default_label)
    df.loc[:, text_column] = df.loc[:, text_column].str.strip()
    
    return df.loc[:, out_columns]


def regexep_replace_closure(re_ptrn, repl):

    compiled_regexp = re.compile(re_ptrn)
    def regexep_replace(s):
        return compiled_regexp.sub(repl, s)

    return regexep_replace
#

multiple_newline_ptn = '[\r\n]+'
mutiple_space_ptrn = '[\t ]+'
non_alpha_ptrn = '[^a-z]+'

mutiple_newline_to_single_newline = regexep_replace_closure(multiple_newline_ptn, u'\n')
multiple_space_to_single_space = regexep_replace_closure(mutiple_space_ptrn, u' ')
str_strip = methodcaller('strip')
str_lower = methodcaller('lower')

space_normalizer = lambda s: toolz.pipe(s, multiple_space_to_single_space, mutiple_newline_to_single_newline, str_strip)

remove_non_alpha = regexep_replace_closure(non_alpha_ptrn, u'')
just_alpha_sequence = lambda s: toolz.pipe(s, str_lower, remove_non_alpha)
