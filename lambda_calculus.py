from curry import curry
from typing import Callable, TypeVar

T = TypeVar('T')

# https://en.wikipedia.org/wiki/Church_encoding#Table_of_functions_on_Church_numerals
@curry
def succ(n:Callable, f:Callable[[T], T], x:T) -> T:
    return f(n(f)(x))


@curry
def plus(m:Callable, n:Callable, f:Callable[[T], T], x:T) -> T:
    return m(f)(n(f)(x)) # m(succ)(n)


@curry
def mult(m:Callable, n:Callable, f:Callable[[T], T]) -> T:
    return m(n(f))


@curry
def exp(m:Callable, n:Callable):
    return n(m)


@curry
def pred(n:Callable, f:Callable, x:T):
    return n(lambda g: lambda h: h(g(f)))(lambda u: x)(lambda u: u)


@curry
def minus(m:Callable, n:Callable):
    return n(pred)(m)
