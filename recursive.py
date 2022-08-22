from typing import Callable, TypeVar

__all__ = ["recursive"]

T = TypeVar('T')
F = Callable[[T],T]

def recursive(recursion:int) -> Callable[[F,int], F]:
    """
    recursive(3, f)(x) = f( f( f(x) ) )
    """
    def recursor_decorator(f:F, *, __recursion:int=recursion) -> F:
        def recursor(arg:T) -> T:
            if __recursion > 1:
                return f(recursor_decorator(f, __recursion = __recursion - 1)(arg))
            return f(arg)
        return recursor
    return recursor_decorator