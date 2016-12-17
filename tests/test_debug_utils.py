import sys
sys.path.append('../')

import debug_utils

import unittest

# log_func_call_closure
# debug
# test_suite_from_test_cases
# run_test_suites

if __name__ == '__main__':

	fn_apply_test_cases = [
							DictMapTest,
							TupleMapTest,
							ForEachTest,
							OrderTuple,
					 	 ]

	fn_apply_test_suite = debug_utils.test_suite_from_test_cases(fn_apply_test_cases)

	test_suites = [
					fn_apply_test_suite,
				  ]

	debug_utils.run_test_suites(test_suites)