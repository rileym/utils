import pdb
from logging import DEBUG
import unittest
import filesystem_utils as fs_utils


# logging

def log_func_call_closure(logger, level = DEBUG, start_msg_template = '{fn_name} was called...', end_msg_template = '{fn_name} finished.'):
    '''Return a function decorator that logs messages when a function is called and when its completed. '''

    def log_func_call(f):

        def f_out(*args, **kwargs):

            start_msg = start_msg_template.format(fn_name = f.__name__)
            logger.log(level, start_msg)
            return f(*args, **kwargs)
            end_msg = end_msg_template.format(fn_name = f.__name__)
            logger.log(level, end_msg)

        return f_out

    return log_func_call


# pdb

def debug(active = True):
    '''Return a function decorator that will set a breakpoint at before the annotated function if ``active`` is True.'''

    def decorator(f):

        def f_new(*args, **kwargs):
            if active:
                pdb.set_trace()

            return f(*args, **kwargs)

        return f_new

    return decorator


# unittest

def test_suite_from_test_cases(test_cases):
    '''Return a test suite from ``test_cases``.'''
    load_tests_from_test_case = lambda test_case: unittest.TestLoader().loadTestsFromTestCase(test_case)
    return unittest.TestSuite( map(load_tests_from_test_case, test_cases) )

def run_test_suites(test_suites, verbosity = 2):
    '''Group ``test_suites`` in a single test suite and run the suite.'''
    master_test_suite = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=verbosity).run(master_test_suite)


class TempDirSetUpTearDownBaseTest(unittest.TestCase):

    @property 
    def dir_path(self):
        return self.temp_dir.dir_

    def next_path(self):
        return self.temp_dir.next_path()

    def setUp(self):
        self.temp_dir = fs_utils.TempDir()
        self.temp_dir.open()

    def tearDown(self):
        self.temp_dir.close()    
