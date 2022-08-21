from curry import curry
from typing import Callable, TypeVar

T = TypeVar('T')

# https://en.wikipedia.org/wiki/Church_encoding#Table_of_functions_on_Church_numerals
@curry
def succ(n:Callable, f:Callable[[T], T], x:T) -> T:
    return f(n(f)(x))
