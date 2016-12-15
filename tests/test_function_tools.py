import sys
sys.path.append('../')

import os

import function_tools as func_tools
from debug_utils import test_suite_from_test_cases, run_test_suites
from abc import ABCMeta, abstractmethod, abstractproperty

import unittest



class DictMapTest(unittest.TestCase):
	
	@property 
	def initial_dict(self):
		keys = 'abcd'
		values = range(len(keys))
		return dict(zip(keys, values))

	@property 
	def expected_output_dict(self):
		keys = self.initial_dict.keys()
		values = map(self.apply_fn, self.initial_dict.values())
		return dict(zip(keys, values))

	@property 
	def apply_fn(self):
		return lambda i: i+1

	def test_basic(self):
		actual_output_dict = func_tools.dict_map(self.apply_fn, self.initial_dict)
		return self.assertEqual(self.expected_output_dict, actual_output_dict)

	def test_empty(self):
		self.assertEqual({}, func_tools.dict_map(self.apply_fn, {}))

class TupleMapTest(unittest.TestCase):

	@property 
	def initial_iterables(self):
		return [range(5), range(5)]

	@property 
	def expected_output_tuple(self):
		return tuple(map(self.apply_fn, *self.initial_iterables))

	@property 
	def apply_fn(self):
		return lambda a,b: a+b

	def test_basic(self):
		actual_output_tuple = func_tools.tuple_map(self.apply_fn, *self.initial_iterables)
		return self.assertEqual(self.expected_output_tuple, actual_output_tuple)

	def test_empty(self):
		self.assertEqual(tuple(), func_tools.tuple_map(self.apply_fn, *[[],[]]))

class ForEachTest(unittest.TestCase):
	
	def setUp(self):
		self.mutable_list = [[1], [1,2], [1,2,3]]
		self.expected_final_mutable_list = [[1,1], [1,2,2], [1,2,3,3]]

	@property 
	def apply_fn(self):
		return lambda list_: list_.append(len(list_))

	def test_basic(self):
		func_tools.for_each(self.apply_fn, self.mutable_list)
		self.assertEqual(self.expected_final_mutable_list, self.mutable_list)

class OrderTuple(unittest.TestCase):
	
	@property 
	def inital_iterable(self):
		return [1,4,2,3,0]

	@property 
	def expected_output_tuple(self):
		return tuple(range(len(self.inital_iterable)))

	def test_basic(self):
		actual_output = func_tools.order_tuple(self.inital_iterable)
		self.assertEqual(self.expected_output_tuple, actual_output)



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