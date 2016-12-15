import sys
sys.path.append('../')

import tempfile
import os

import filesystem_utils as fs_utils
from debug_utils import test_suite_from_test_cases, run_test_suites
from abc import ABCMeta, abstractmethod, abstractproperty

import unittest

WINDOWS_NAME = u'nt'

class TempDirTestBase(unittest.TestCase):

    def setUp(self):
        self.expected_length = 50

    def _objects(self):
        return xrange(self.expected_length)

class TempDirTestNoSetUp(TempDirTestBase):

    def test_in_context_manager_open_close(self):

        with fs_utils.TempDir() as temp_dir:

            self.assertTrue(fs_utils.dir_exists(temp_dir._dir))
        
        self.assertFalse(fs_utils.dir_exists(temp_dir._dir))

    def test_manual_user_open_close(self):
        
        temp_dir = fs_utils.TempDir()
        temp_dir.open()
        self.assertTrue( fs_utils.dir_exists(temp_dir._dir) )
        temp_dir.close()
        self.assertFalse( fs_utils.dir_exists(temp_dir._dir) )

    def test_length(self):

        with fs_utils.TempDir() as temp_dir:

            for obj, path in zip(self._objects(), temp_dir.iter_candidate_paths()):
                fs_utils.dump_pkl(obj, path)

            self.assertEqual(self.expected_length, len(temp_dir))

        with self.assertRaises(OSError):
            len(temp_dir)

class TempDirTestWithSetUp(TempDirTestBase):

    def setUp(self):
        super(TempDirTestWithSetUp, self).setUp()
        self.temp_dir = fs_utils.TempDir()
        self.temp_dir.open()

    def tearDown(self):
        self.temp_dir.close()

    def test_next_path(self):     
        paths = []
        for obj in self._objects():
            path = self.temp_dir.next_path()
            fs_utils.dump_pkl(obj, path)
            paths.append(path)

        self.assertEquals( set(self._objects()), set(self._load_stored_objects(paths)) )

    def _load_stored_objects(self, paths):
        return [fs_utils.load_pkl(path) for path in paths]

    def test_iter_candidate_paths(self):
        
        paths = []
        for obj, path in zip(self._objects(), self.temp_dir.iter_candidate_paths()):
            paths.append(path)
            fs_utils.dump_pkl(obj, path)

        self.assertEquals(self.expected_length, len(self.temp_dir))
        self.assertEquals( set(self._objects()), set(self._load_stored_objects(paths)) )

    def test_iter_paths(self):
        
        paths = []
        for obj, path in zip(self._objects(), self.temp_dir.iter_candidate_paths()):
            paths.append(path)
            fs_utils.dump_pkl(obj, path)

        self.assertEquals(self.expected_length, len(self.temp_dir))
        self.assertEquals( set(self._objects()), set(self._load_stored_objects(paths)) )
        self.assertEquals( set(self.temp_dir.iter_paths()), set(paths) )

class BaseTempDirSetUpTearDown(unittest.TestCase):

	@property 
	def _dummy_path_templates(self):
		return []

	@property 
	def _dummy_paths(self):
		filled_in_paths = map(self._fill_in_base_dir, self._dummy_path_templates)
		return map(os.path.normpath, filled_in_paths)

	def _fill_in_base_dir(self, template):
		return template.format(base_dir = self.temp_dir.dir_)

	def _redundant_safe_makedirs(self, dir_path):
		try:
			os.makedirs(dir_path)
		except os.error as e:
			pass		

	def _build_dummy_files(self):

		for path in self._dummy_paths:
			dir_path = os.path.dirname(path)
			self._redundant_safe_makedirs(dir_path)
			fs_utils.touch(path)

	def setUp(self):
		self.temp_dir = fs_utils.TempDir()
		self.temp_dir.open()
		self._build_dummy_files()

	def tearDown(self):
		self.temp_dir.close()	

class NormjoinTest(BaseTempDirSetUpTearDown):

	def setUp(self):
		super(NormjoinTest, self).setUp()
		self._path_to_pieces_examples = self._get_path_to_pieces_dict()

	@property 
	def _dummy_path_templates(self):
		return _dummy_path_templates_to_peices_templates_dict.keys()

	@property 
	def _dummy_path_templates_to_peices_templates_dict(self):
		return {
				u'{base_dir}/a/b/c/d.txt' : [
											 ['{base_dir}/', 'a//b/', './c/d.txt'],
											 ['{base_dir}/a/b//', '../b/c/d.txt'],
											 ['{base_dir}\\', 'a/b/', './c/d.txt']
					 						],
			}	


	def _fill_in_pieces_template(self, pieces_templates):
		pieces_templates = list(pieces_templates)
		pieces_templates[0] = self._fill_in_base_dir(pieces_templates[0])
		return pieces_templates 

	def _get_path_to_pieces_dict(self):

		paths_to_pieces_dict = dict()
		for path_template, pieces_templates in self._dummy_path_templates_to_peices_templates_dict.iteritems():

			path = self._fill_in_base_dir(path_template)
			path = os.path.normpath(path)
			pieces = [self._fill_in_pieces_template(pieces_template) for pieces_template in pieces_templates]
			paths_to_pieces_dict[path] = pieces

		return paths_to_pieces_dict

	@property 
	def _dummy_paths(self):
		path_templates = self._dummy_path_templates_to_peices_templates_dict.keys()
		return map(self._fill_in_base_dir, path_templates)

	def test_normjoins(self):
		for target_path, pieces_lists in self._path_to_pieces_examples.iteritems():
			for pieces_list in pieces_lists:
				self.assertEqual(target_path, fs_utils.normjoin(*pieces_list))

class ListpathsTest(BaseTempDirSetUpTearDown):

	@property 
	def _dummy_path_templates(self):
		return [
			u'{base_dir}/a.txt',
			u'{base_dir}/b.txt',
			u'{base_dir}/c.txt',
			u'{base_dir}/d.txt',
			u'{base_dir}/e/a.txt',
		]

	def _is_truncated_subpath(self, full_path, candidate_truncated_subpath):
		return full_path.find(candidate_truncated_subpath) == 0

	def test_listpaths_basic(self):
		normed_paths = map(os.path.normpath, self._dummy_paths)
		listed_paths = fs_utils.listpaths(self.temp_dir.dir_)
		for listed_path in listed_paths:
			listed_path_is_correct = any( self._is_truncated_subpath(normed_path, listed_path) for normed_path in normed_paths )
			self.assertTrue(listed_path_is_correct) 

class ListpathsEmptyTest(BaseTempDirSetUpTearDown):

	@property 
	def _dummy_path_templates(self):
		return []

	def test_empty_listpaths(self):
		self.assertEqual([], fs_utils.listpaths(self.temp_dir.dir_))

class DirectoryFilenameInventoryBaseTest(BaseTempDirSetUpTearDown):

	@property
	def basename_pred(self):
		return None

	def test_directory_filename_inventory(self):
		actual_filenames = set(self._expected_filenames)
		found_filenames = set(fs_utils.directory_filename_inventory(self.temp_dir.dir_, basename_pred = self.basename_pred))
		self.assertEqual(actual_filenames, found_filenames)

class DirectoryFilenameInventoryBasicTest(DirectoryFilenameInventoryBaseTest):

	@property 
	def _dummy_path_templates(self):
		return [
			u'{base_dir}/a/a.txt',
			u'{base_dir}/a/b.txt',
			u'{base_dir}/b/a.txt',
			u'{base_dir}/a.txt',
			u'{base_dir}/b.txt',
			u'{base_dir}/c.csv'
		]

	@property
	def _expected_filenames(self):
		return [
			u'a.txt',
			u'b.txt',
			u'c.csv'
		]

class DirectoryFilenameInventoryPredTest(DirectoryFilenameInventoryBasicTest):

	@property 
	def basename_pred(self):
		return lambda bn: u'b' in bn

	@property
	def _expected_filenames(self):
		return [u'b.txt']

class DirectoryFilenameInventoryEmptyTest(DirectoryFilenameInventoryBaseTest):

	@property 
	def _dummy_path_templates(self):
		return []

	@property
	def _expected_filenames(self):
		return []

class FilepathMacthingReTest(BaseTempDirSetUpTearDown):

	@property 
	def _dummy_path_templates(self):
		return [
			u'{base_dir}/a/a.txt',
			u'{base_dir}/a/b.txt',
			u'{base_dir}/a.txt',
			u'{base_dir}/b.txt',
			u'{base_dir}/c.csv',
			u'{base_dir}/d.csv',
			u'{base_dir}/e.csv',						
		]

	def test_no_match(self):
		returned_paths = set(fs_utils.filepaths_matching_re(self.temp_dir.dir_, u'not_a_match$'))
		self.assertEquals(set(), returned_paths)

	def test_basic_re(self):
		expected_paths = set(self._dummy_paths[-3:])
		returned_paths = set(fs_utils.filepaths_matching_re(self.temp_dir.dir_, u'^.+\.csv$'))
		self.assertEquals(expected_paths, returned_paths)

class DirExistsTestBase(BaseTempDirSetUpTearDown):

	@property 
	def _dummy_path_templates(self):
		return [
				u'{base_dir}/a.txt'
			   ]

	@property 
	def _fake_dir(self):
		fake_dir = fs_utils.normjoin(self._dummy_paths[0], u'fake')
		return fake_dir

class DirExistsTest(DirExistsTestBase):

	def test_exists_when_exists(self):
		self.assertTrue(fs_utils.dir_exists(self.temp_dir.dir_))

	def test_exists_when_not_exists(self):
		self.assertFalse(fs_utils.dir_exists(self._fake_dir))

	def test_exists_when_file(self):
		self.assertFalse(fs_utils.dir_exists(self._dummy_paths[0]))

class DirDoesNotExistTest(DirExistsTest):

	def test_not_exists_when_exists(self):
		self.assertFalse(fs_utils.dir_does_not_exist(self.temp_dir.dir_))

	def test_not_exists_when_not_exists(self):
		self.assertTrue(fs_utils.dir_does_not_exist(self._fake_dir))

	def test_not_exists_when_file(self):
		self.assertFalse(fs_utils.dir_does_not_exist(self._dummy_paths[0]))

class DirIsEmptyTest(BaseTempDirSetUpTearDown):

	def test_is_empty_when_empty(self):
		self.assertTrue(fs_utils.dir_is_empty(self.temp_dir.dir_))

	def test_is_empty_when_not_exists(self):
		fake_dir = fs_utils.normjoin(self.temp_dir.dir_, u'fake')
		with self.assertRaises(WindowsError):
			fs_utils.dir_is_empty(fake_dir)

	def _set_up_add_file(self):
		new_filename = u'a.txt'
		new_path = fs_utils.normjoin(self.temp_dir.dir_, new_filename)
		fs_utils.touch(new_path)

	def test_is_empty_when_non_empty(self):
		self._set_up_add_file()
		self.assertFalse(fs_utils.dir_is_empty(self.temp_dir.dir_))

	def test_is_empty_when_non_empty(self):
		self._set_up_add_file()
		self.assertFalse(fs_utils.dir_is_empty(self.temp_dir.dir_))

	def test_is_empty_when_non_directory(self):
		self._set_up_add_file()
		filepath = fs_utils.listpaths(self.temp_dir.dir_)[0]
		with self.assertRaises(WindowsError):
			fs_utils.dir_is_empty(filepath)

	# def test_exists_when_file(self):
	# 	self.assertFalse(fs_utils.dir_exists(self._dummy_paths[0]))	
	# dir is empty
	# dir is not empty
	# dir does not exist
	# is a file

class RemoveFileTest(BaseTempDirSetUpTearDown):
	pass
	# remove files
	# remove dir
	# remove non-existant

class RemoveDir(BaseTempDirSetUpTearDown):
	pass
	# remove dir
	# remove file
	# remove non-existant

if __name__ == '__main__':

	tempdir_test_cases = [
							TempDirTestBase,
							TempDirTestNoSetUp,
							TempDirTestWithSetUp
					 	 ]

	path_manipulation_test_cases = [
									NormjoinTest,
				 				   ]

	directory_inventory_test_cases = [
										ListpathsTest,
										ListpathsEmptyTest,
										DirectoryFilenameInventoryBasicTest,
										DirectoryFilenameInventoryPredTest,
										DirectoryFilenameInventoryEmptyTest,
										FilepathMacthingReTest,
									 ]

	directory_status_test_cases  = [
									DirExistsTest,
									DirIsEmptyTest,
									DirDoesNotExistTest,
								   ]

   fs_remove_actions_test_cases = [



   								  ]

   fs_file_create_and_read_test_cases = [



   										]

	tempdir_test_suit = test_suite_from_test_cases(tempdir_test_cases)
	path_manipulation_test_suite = test_suite_from_test_cases(path_manipulation_test_cases)
	directory_inventory_test_suite = test_suite_from_test_cases(directory_inventory_test_cases)
	directory_status_test_suite = test_suite_from_test_cases(directory_status_test_cases)
	fs_remove_actions_test_suite = test_suite_from_test_cases(fs_remove_actions_test_case)
	fs_file_create_and_read_suite = test_suite_from_test_cases(fs_file_create_and_read_test_cases)

	test_suites = [
					tempdir_test_suit,
					path_manipulation_test_suite,
					directory_inventory_test_suite,
					directory_status_test_suite,
					remove_test_suite,
					fs_remove_actions_test_suite,
					fs_file_create_and_read_suite
				  ]

	run_test_suites(test_suites)

# normjoin
# listpaths
# directory_filename_inventory
# filepaths_matching_re
# dir_is_empty
# dir_exists
# dir_does_not_exist


# remove_file
# remove_dir
# touch
# load_pkl
# dump_pkl
# load_json
