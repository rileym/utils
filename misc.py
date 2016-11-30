import re
import unittest
import json


#
# MOVE TO RELEVANT DOMAIN
#

def format_df_for_review(df, id_columns, text_column, label_column, rank_column = None, default_label = u''):

    df = df.copy()
    
    out_columns = id_columns + [text_column] + [label_column]
    
    if rank_column:
        df = df.sort_values(rank_column, ascending = False)
        out_columns.insert(len(id_columns), rank_column)
    
    df[label_column] = unicode(default_label)
    df.loc[:, text_column] = df.loc[:, text_column].str.strip()
    
    return df.loc[:, out_columns]


newline_ptn = '[\r\n]+'
newline_re = re.compile(newline_ptn)
space_ptn = '[\t ]+'
space_re = re.compile(space_ptn)
def space_normalizer(s):
    return newline_re.sub('\n', space_re.sub(' ', s)).strip()


def just_alpha_sequence(raw_str):
    
    non_alpha_ptrn = '[^a-z]+'
    return re.sub(non_alpha_ptrn, u'', raw_str.lower())

#
# unit testing
#

def load_json(path):
    with open(path, 'rb') as f:
        return json.load(f)

def test_suite_from_test_cases(test_cases):

    load_tests_from_test_case = lambda test_case: unittest.TestLoader().loadTestsFromTestCase(test_case)
    return unittest.TestSuite( map(load_tests_from_test_case, test_cases) )