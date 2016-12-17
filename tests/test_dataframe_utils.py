import sys
sys.path.append('../')

import pandas as pd

import dataframe_utils as df_utils
from filesystem_utils import TempDir
from debug_utils import test_suite_from_test_cases, run_test_suites, TempDirSetUpTearDownBaseTest

import unittest

# drop_columns_by_name_predicate
# keep_columns_by_name_predicate
# partition_df
# vstack_dfs
# hstack_dfs
# index_to_columns

# df_select_gen
# standard_csv_update
# standard_chunked_csv_load
# standard_chunked_csv_load_iter
# standard_csv_load
# standard_csv_save

# stack_load_txt_files

basic_examples_nrows = 10
basic_example_data_dict = {
	'column_a': range(basic_examples_nrows),
	'column_b': list('abcdefghijklmnopqrstuzwxyz')[:basic_examples_nrows],
	'the odd column': range(5, 5 + basic_examples_nrows),
}
basic_example_dataframe =  pd.DataFrame(basic_example_data_dict)

old_column_names = basic_example_data_dict.keys()
new_column_names = map(lambda s: s.upper(), basic_example_data_dict.keys())
rename_map = dict(zip(old_column_names, new_column_names))
basic_example_dataframe2 = basic_example_dataframe.rename(columns = rename_map)


def dfs_are_equal(df1, df2):
	return df1.equals(df2)

class DropKeepColumnByNamePredicateTest(unittest.TestCase):
	
	def test_basic_drop_predicate(self):
		expected_df = basic_example_dataframe.drop(labels = ['column_a', 'column_b'], axis = 1)
		actual_df = df_utils.drop_columns_by_name_predicate(basic_example_dataframe, lambda name:'_' in name)
		self.assertTrue(dfs_are_equal(expected_df, actual_df))

	def test_basic_keep_predicate(self):
		expected_df = basic_example_dataframe.drop(labels = ['the odd column'], axis = 1)
		actual_df = df_utils.keep_columns_by_name_predicate(basic_example_dataframe, lambda name:'_' in name)
		self.assertTrue(dfs_are_equal(expected_df, actual_df))

	def test_all_match_drop_predicate(self):
		expected_df = basic_example_dataframe.loc[:,[]]
		actual_df = df_utils.drop_columns_by_name_predicate(basic_example_dataframe, lambda name:'column' in name)
		self.assertTrue(dfs_are_equal(expected_df, actual_df))		

	def test_no_match_keep_predicate(self):
		expected_df = basic_example_dataframe.loc[:,[]]
		actual_df = df_utils.keep_columns_by_name_predicate(basic_example_dataframe, lambda name:'notinany!' in name)
		self.assertTrue(dfs_are_equal(expected_df, actual_df))


class PartitionDfTest(unittest.TestCase):
	
	def test_basic_partition(self):
		N_PARTITIONS = 4
		df_partitions = list(df_utils.partition_df(basic_example_dataframe, n_partitions = N_PARTITIONS))
		self.assertEqual(N_PARTITIONS, len(df_partitions))
		self.assertTrue(dfs_are_equal(basic_example_dataframe, df_utils.vstack_dfs(df_partitions)))

class VstackDfTest(unittest.TestCase):
	
	def test_basic_vstact(self):
		to_stack = [basic_example_dataframe, basic_example_dataframe, basic_example_dataframe]
		stacked = df_utils.vstack_dfs(to_stack)
		split = list(df_utils.partition_df(stacked, n_partitions = len(to_stack)))

		for part in split:
			self.assertTrue(dfs_are_equal(basic_example_dataframe, part.reset_index(drop = True)))	

class HstackDfTest(unittest.TestCase):

	def test_basic_hstack(self):

		to_hstack = [basic_example_dataframe, basic_example_dataframe2]
		hstacked = df_utils.hstack_dfs(to_hstack)
		self.assertEqual(set(old_column_names + new_column_names), set(hstacked.columns))
		self.assertTrue(dfs_are_equal(basic_example_dataframe, hstacked.loc[:, basic_example_dataframe.columns]))
		self.assertTrue(dfs_are_equal(basic_example_dataframe2, hstacked.loc[:, basic_example_dataframe2.columns]))

class IndexToColumnsTest(unittest.TestCase):
	
	def test_index_to_columns_basic(self):
		INDEX_NAME = 'blah_blah'
		df_with_index_column = df_utils.index_to_columns(basic_example_dataframe, new_index_name = INDEX_NAME)
		self.assertTrue(dfs_are_equal(basic_example_dataframe[old_column_names], df_with_index_column[old_column_names]))
		self.assertEqual(list(basic_example_dataframe.index), list(df_with_index_column.loc[:, INDEX_NAME]))

class DfSelectGenTest(unittest.TestCase):

	def _df_from_rows(self, rows, column_names):
		return pd.DataFrame.from_records(data = rows, columns = column_names)

	def test_basic(self):
		column_subset = [old_column_names[0], old_column_names[-1]]
		select_gen = list(df_utils.df_select_gen(basic_example_dataframe, col_subset = column_subset, squeeze = False))
		recreated_df = self._df_from_rows(select_gen, column_subset)

		self.assertEqual(basic_examples_nrows, len(select_gen))
		self.assertTrue( all( isinstance(row, tuple) for row in select_gen ) )
		self.assertTrue(dfs_are_equal(basic_example_dataframe.loc[:, column_subset], recreated_df))
	
	def test_single_column_with_squeeze(self):
		column_subset = [old_column_names[0]]
		select_gen = list(df_utils.df_select_gen(basic_example_dataframe, col_subset = column_subset, squeeze = True))

		self.assertEqual(basic_examples_nrows, len(select_gen))
		self.assertTrue( all( not isinstance(row, tuple) for row in select_gen ) )
		self.assertEqual(list(basic_example_dataframe.loc[:, column_subset[0]].values), select_gen)		


# class TempDirSetUpTearDownBaseTest(unittest.TestCase):

# 	@property 
# 	def dir_path(self):
# 		return self.temp_dir.dir_ 

# 	def setUp(self):
# 		self.temp_dir = TempDir()
# 		self.temp_dir.open()

# 	def tearDown(self):
# 		self.temp_dir.close()


class StandardCsvUpdate(TempDirSetUpTearDownBaseTest):
	# standard_csv_update
	pass

class StandardChunkedCsvLoad(TempDirSetUpTearDownBaseTest):
	# standard_chunked_csv_load
	pass

class StandardChunkedCsvLoadIter(TempDirSetUpTearDownBaseTest):
	# standard_chunked_csv_load_iter
	pass

class StandardCsvLoad(TempDirSetUpTearDownBaseTest):
	# standard_csv_load
	pass

class StandardCsvSave(TempDirSetUpTearDownBaseTest):
	# standard_csv_save
	pass



if __name__ == '__main__':

	column_name_predicate_test_cases = [
										DropKeepColumnByNamePredicateTest,
					 	 			   ]

 	df_manipulation_test_cases = [
									PartitionDfTest,
									VstackDfTest,
									HstackDfTest,
									IndexToColumnsTest,
 								  ]

 	df_iteration_test_cases = [
 								DfSelectGenTest,
 							  ]

 	df_io_test_cases = [
			 			StandardCsvUpdate,
						StandardChunkedCsvLoad,
						StandardChunkedCsvLoadIter,
						StandardCsvLoad,
						StandardCsvSave,
					   ]

	column_name_predicate_test_suite = test_suite_from_test_cases(column_name_predicate_test_cases)
	df_manipulation_test_suite = test_suite_from_test_cases(df_manipulation_test_cases)
	df_iteration_test_suite = test_suite_from_test_cases(df_iteration_test_cases)
	df_io_test_suite = test_suite_from_test_cases(df_io_test_cases)

	test_suites = [
					column_name_predicate_test_suite,
					df_manipulation_test_suite,
					df_iteration_test_suite,
					df_io_test_suite
				  ]

	run_test_suites(test_suites)


