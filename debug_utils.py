import pdb
from logging import DEBUG

#
# Debug / logging
#

def log_func_call_closure(logger, level = DEBUG, start_msg_template = '{fn_name} was called...', end_msg_template = '{fn_name} finished.'):

    def log_func_call(f):

        def f_out(*args, **kwargs):

            start_msg = start_msg_template.format(fn_name = f.__name__)
            logger.log(level, start_msg)
            return f(*args, **kwargs)
            end_msg = end_msg_template.format(fn_name = f.__name__)
            logger.log(level, end_msg)

        return f_out

    return log_func_call

def debug(active = True):

    def decorator(f):

        def f_new(*args, **kwargs):
            if active:
                pdb.set_trace()

            return f(*args, **kwargs)

        return f_new

    return decorator