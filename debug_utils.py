import pdb
from logging import DEBUG
import unittest

# Logging

def log_func_call_closure(logger, level = DEBUG, start_msg_template = '{fn_name} was called...', end_msg_template = '{fn_name} finished.'):
    '''
    Returns a function decorator that logs messages when a function is called and when its completed. 
    '''
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
    '''
    Returns a function decorator that will set a breakpoint at this function if 'active' is True.
    '''
    def decorator(f):

        def f_new(*args, **kwargs):
            if active:
                pdb.set_trace()

            return f(*args, **kwargs)

        return f_new

    return decorator

# unittest

def test_suite_from_test_cases(test_cases):
    '''
    Create and return a test suite from test_cases.
    '''
    load_tests_from_test_case = lambda test_case: unittest.TestLoader().loadTestsFromTestCase(test_case)
    return unittest.TestSuite( map(load_tests_from_test_case, test_cases) )