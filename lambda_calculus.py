from typing import Callable, TypeVar

__all__ = ["succ", "plus", "mult", "exp", "pred", "minus"]
T = TypeVar('T')
F = Callable[[T], T]
Functor = Callable[[F], F]
Recusive = Callable[[F, int], F]

# https://en.wikipedia.org/wiki/Church_encoding#Table_of_functions_on_Church_numerals

succ:Callable[[Recusive], Callable[[F], T]] \
    = lambda n: lambda f: lambda x: f(n(f)(x))

plus:Callable[[Recusive], Callable[[Recusive], Callable[[F], Callable[[T], T]]]] \
    = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x)) # m(succ)(n)

mult:Callable[[Recusive], Callable[[Recusive], Functor]] \
    = lambda m: lambda n: lambda f: m(n(f))

exp:Callable[[Recusive], Callable[[Recusive], Functor]] \
    = lambda m: lambda n: n(m)

pred:Callable[[Recusive], Callable[[F], Callable[[T], T]]] \
    = lambda n: lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda u: x)(lambda u: u)

minus:Callable[[Recusive], Callable[[Recusive], Functor]]\
     = lambda m: lambda n: n(pred)(m)
