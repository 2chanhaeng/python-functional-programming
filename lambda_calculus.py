from typing import Callable, TypeVar

T = TypeVar('T')

# https://en.wikipedia.org/wiki/Church_encoding#Table_of_functions_on_Church_numerals

succ:Callable[[Callable], Callable[[Callable[[T], T]], Callable[[T], T]]] \
    = lambda n: lambda f: lambda x: f(n(f)(x))

plus:Callable[[Callable], Callable[[Callable], Callable[[Callable[[T], T]], Callable[[T], T]]]] \
    = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))

mult:Callable[[Callable], Callable[[Callable], Callable[[Callable[[T], T]], T]]] \
    = lambda m: lambda n: lambda f: m(n(f))

exp:Callable[[Callable], Callable[[Callable]]] \
    = lambda m: lambda n: n(m)

pred:Callable[[Callable], Callable[[Callable[[T], T]], Callable[[T], T]]] \
    = lambda n: lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda u: x)(lambda u: u)

minus:Callable[[Callable], Callable[[Callable]]]\
     = lambda m: lambda n: n(pred)(m)
