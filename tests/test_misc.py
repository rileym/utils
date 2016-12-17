import sys
sys.path.append('../')

import misc
from debug_utils import test_suite_from_test_cases, run_test_suites

import unittest

# transform_date
# format_df_for_review
# regexep_replace_closure
# space_normalizer
# remove_non_alpha
# just_alpha_sequence

if __name__ == '__main__':

	fn_apply_test_cases = [
							DictMapTest,
							TupleMapTest,
							ForEachTest,
							OrderTuple,
					 	 ]

	fn_apply_test_suite = test_suite_from_test_cases(fn_apply_test_cases)

	test_suites = [
					fn_apply_test_suite,
				  ]

	run_test_suites(test_suites)