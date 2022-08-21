from curry import curry
from typing import Callable, Any

__all__ = ["recursive"]

@curry
def recursive(recursion:int, f:Callable):
    """
    recursive(3, f)(x) = f( f( f(x) ) )
    """
    def operator(*args:Any, **kwargs:Any):
        if recursion > 1:
            return f(recursive(recursion - 1, f)(*args, **kwargs))
        return f(*args, **kwargs)
    return operator