from recursive import recursive
from typing import Callable, TypeVar

__all__ = ["succ", "plus", "mult", "exp", "pred", "minus"]
T = TypeVar('T')
F = Callable[[T], T]
Functor = Callable[[F], F]
Recusive = int

# https://en.wikipedia.org/wiki/Church_encoding#Table_of_functions_on_Church_numerals

succ:Callable[[Recusive], Callable[[F], T]] \
    = lambda n: lambda f: lambda x: f(recursive(n)(f)(x))

plus:Callable[[Recusive], Callable[[Recusive], Callable[[F], Callable[[T], T]]]] \
    = lambda m: lambda n: lambda f: lambda x: recursive(m)(f)(recursive(n)(f)(x)) # m(succ)(n)

mult:Callable[[Recusive], Callable[[Recusive], Functor]] \
    = lambda m: lambda n: lambda f: recursive(m)(recursive(n)(f))

exp:Callable[[Recusive], Callable[[Recusive], Functor]] \
    = lambda m: lambda n: recursive(n)(recursive(m))

pred:Callable[[Recusive], Callable[[F], Callable[[T], T]]] \
    = lambda n: lambda f: lambda x: recursive(n)(lambda g: lambda h: h(g(f)))(lambda u: x)(lambda u: u)

minus:Callable[[Recusive], Callable[[Recusive], Functor]]\
     = lambda m: lambda n: recursive(n)(pred)(recursive(m))
