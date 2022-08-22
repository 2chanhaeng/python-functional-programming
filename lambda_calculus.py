from recursive import recursive
from typing import Callable, TypeVar, ParamSpec

__all__ = ["succ", "plus", "mult", "exp", "pred", "minus", "true", "false", "pair", "first", "second"]

T, _S = TypeVar('T'), TypeVar('S')
P, Q = ParamSpec('P'), ParamSpec('P')
F = Callable[[T], T]
Functor = Callable[[F], F]
Recusive = int
Pair = Callable[P,Callable[Q,Callable[[Callable[P,Callable[Q,T]]],T]]]

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

true :Callable[[T], Callable[[_S], T]] = lambda a: lambda b: a

false:Callable[[T], Callable[[_S], _S]] = lambda a: lambda b: b

pair:Pair = lambda a: lambda b: lambda h: h(a)(b)

first :Callable[[Pair],T] = lambda p: p(true)

second:Callable[[Pair],T] = lambda p: p(false)