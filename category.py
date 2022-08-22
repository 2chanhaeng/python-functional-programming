from lambda_calculus import *
from recursive import recursive
from typing import Callable, TypeVar, ParamSpec, Any
P, Q = ParamSpec('P'), ParamSpec('P')
T = TypeVar('T')
F = Callable[[T],T]
Functor = Callable[[F],F]
Recusive = int
Pair = Callable[P,Callable[Q,Callable[[Callable[P,Callable[Q,T]]],T]]]

class Category:
    value:Callable[[T], Callable[[Callable], T]] = lambda v: (lambda h: h(v))
    const:Callable[[T], Callable[[Callable], T]] = lambda v: lambda u: v
    inc:Callable[[F], Callable[[Callable], T]] = lambda f: lambda g: lambda h: h(g(f))
    succ:Callable[[Recusive], Callable[[F], T]] \
        = lambda f: lambda x: lambda n: f(recursive(n)(f)(x))
    
    def __init__(self, f:F, x:T):
        self.__f = f
        self.const = Category.const(x)
        self.init = Category.value(x)
        self.inc = Category.inc(f)
        self.succ = Category.succ(self.inc)(self.init)
        self.plus:Callable[[Recusive], Callable[[Recusive], T]] \
            = lambda m: lambda n: recursive(m)(self.inc)(recursive(n)(self.inc)(self.init))
        self.curr_succ:Callable[[Pair], Pair] = lambda p: pair(second(p))(self.inc(second(p)))