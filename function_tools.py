from itertools import izip

def dict_map(f, d):
    return dict( (k, f(v)) for k,v in d.iteritems() )

def tuple_map(fn, iterable):
    return tuple(map(fn, iterable))

def order_tuple(t, **sorted_kwargs):
    return tuple(sorted(t, **sorted_kwargs))
    
def for_each(fn, *iterables):
    for args in izip(*iterables):
        fn(*args)

