from itertools import izip

def dict_map(f, d):
	'''
	Returns a new ditionary with key-value pairs (k, f(d[k])) where k is a key in d.
	'''
	return dict( (k, f(v)) for k,v in d.iteritems() )

def tuple_map(fn, *iterables):
	'''
	Similar to map builtin, but returns a tuple instead of list.
	'''
	return tuple(map(fn, *iterables))

def order_tuple(t, **sorted_kwargs):
	'''
	Similar to builtin sorted but returns a tuple.
	'''
	return tuple(sorted(t, **sorted_kwargs))
    
def for_each(fn, *iterables):
	'''
	Similar to map builtin but assumes fn doesn't return anything useful and instead relies on side effects. Returns None.
	'''
	for args in izip(*iterables):
	    fn(*args)

