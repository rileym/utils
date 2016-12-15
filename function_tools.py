from itertools import izip

def dict_map(f, d):
	'''Return a new dictionary with key-value pairs (k, f(d[k])) where k is a key in d.'''
	return dict( (k, f(v)) for k,v in d.iteritems() )

def tuple_map(fn, *iterables):
	'''Apply function to every item of iterable and return a tuple of the results.'''
	return tuple(map(fn, *iterables))

def order_tuple(iterable, **sorted_kwargs):
	'''
	Return a new sorted tuple from the items in iterable.

	sorted_kwargs are passed to builtin sorted. See sorted doc for details.
	'''
	
	return tuple(sorted(iterable, **sorted_kwargs))
    
def for_each(fn, *iterables):
	'''Apply function to every item of iterable and return no value. Relies on side effects.'''
	for args in izip(*iterables):
	    fn(*args)

