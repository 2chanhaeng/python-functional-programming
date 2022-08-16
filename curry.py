from functools import partial
from inspect import getfullargspec

__all__ = ["curry"]

# https://medium.com/@aeshghi/functional-programming-python-curry-decorator-function-756fdae3036f
def curry(wrapped_fn, arity=None):
    n_args = len(getfullargspec(wrapped_fn).args) if arity is None else arity
    def curried(*args, **kwargs):
        len_args = len(args) + len(kwargs)
        if n_args == len_args:
            return wrapped_fn(*args, **kwargs)

        return curry(partial(wrapped_fn, *args, **kwargs), n_args - len_args)
    return curried