from functools import partial
from inspect import getfullargspec

__all__ = ["curry"]

# https://medium.com/@aeshghi/functional-programming-python-curry-decorator-function-756fdae3036f
def curry(wrapped_fn, arity=None):
    n_args = len(getfullargspec(wrapped_fn).args) if arity is None else arity
    def curried(first_arg, *args):
        if n_args == len(args) + 1:
            return wrapped_fn(first_arg, *args)

        return curry(partial(wrapped_fn, first_arg, *args), n_args - (1 + len(args)))
    return curried