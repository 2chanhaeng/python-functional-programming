from typing import List, Iterable, TypeVar, Any, Callable, Optional, TypeAlias, Iterator
from functools import reduce
from inspect import signature, getfullargspec

__all__ = ["Chain", "LightChain"]

T, S = TypeVar('T'), TypeVar('S')
MapHandler = Callable[[Any], T]|Callable[[Any, int], T]|Callable[[Any, int, Iterable], T]
FilterHandler = Callable[[Any], bool]|Callable[[Any, int], bool]|Callable[[Any, int, Iterable], bool]
ReduceHandler = Callable[[Any, Any], T]|Callable[[Any, Any, int], T]|Callable[[Any, Any, int, Iterable], T]

class Chain(tuple):
    def __init__(self, iterable:Iterable|None) -> None:
        tuple.__init__(iterable)

    def map(self, handler:MapHandler, start:bool=0) -> 'Chain[Any]':
        """
        handler(< take no args >) => Chain[handler() * len(origin_Chain)]

        handler(one) => Chain[handler(element), ...]

        handler(one, two) => Chain[handler(element, index), ...]

        handler(one, two, tree) => Chain[handler(element, index, origin_Chain), ...]

        handler(one, two, tree, *more) => Chain[handler(element, index, origin_Chain, *([None] * len(more))),...]
        """
        match len(getfullargspec(handler).args):
            case 0:
                return Chain([handler() for i in range(len(self))])
            case 1:
                return Chain(map(handler, self))
            case 2:
                return Chain(map(lambda x: handler(x[1], x[0]), enumerate(self, start)))
            case 3:
                return Chain(map(lambda x: handler(x[1], x[0], self), enumerate(self, start)))
            case length:
                return Chain(map(lambda x: handler(x[1], x[0], self, *([None] * (length - 3))), enumerate(self, start)))

    def filter(self, handler:FilterHandler, start:int=0) -> 'Chain[Any]':
        """
        handler(< take no args >) => Chain[element if handler()]

        handler(one) => Chain[element if handler(lement)]

        handler(one, two) => Chain[element if handler(element, index)]

        handler(one, two, tree) => Chain[element if handler(element, index, origin_Chain)]
        
        handler(one, two, tree, *more) => Chain[element if handler(element, index, origin_Chain, *([None] * len(more)))]
        """
        match len(getfullargspec(handler).args):
            case 0:
                return Chain(i for i in self if handler())
            case 1:
                return Chain(filter(handler, self))
            case 2:
                return Chain(x for i, x in enumerate(self, start) if handler(x, i))
            case 3:
                return Chain(x for i, x in enumerate(self, start) if handler(x, i, self))
            case length:
                return Chain(x for i, x in enumerate(self, start) if handler(x, i, self, *([None] * (length - 3))))

    def reduce(self, handler:ReduceHandler, initializer:T|None=None, start:int=0) -> T:
        """
        handler(one) => handler(previous)

        handler(one, two) => handler(previous, element)

        handler(one, two, tree) => handler(previous, element, index)

        handler(one, two, tree, four) => handler(previous, element, index, origin_Chain)
        
        handler(one, two, tree, four, *more) => handler(previous, element, index, origin_Chain, *([None] * len(more))
        """
        iterator = iter(self)
        is_init = 0
        if initializer == None:
            initializer = next(iterator)
            is_init = 1
        match len(getfullargspec(handler).args):
            case 1:
                return reduce(lambda initializer, _: handler(initializer), iterator, initializer)
            case 2:
                return reduce(handler, iterator, initializer)
            case 3:
                return reduce(lambda init, x: handler(init, x[1], x[0]), enumerate(iterator, start + is_init))
            case 4:
                return reduce(lambda init, x: handler(init, x[1], x[0], self), enumerate(iterator, start + is_init))
            case length:
                return reduce(lambda init, x: handler(init, x[1], x[0], self, *([None] * (length - 3))), enumerate(self, start + is_init))


class LightChain(tuple):
    def __init__(self, iterable:Iterable|None) -> None:
        tuple.__init__(iterable)

    def map(self, handler:MapHandler) -> 'LightChain[Any]':
        """
        LightChain[handler(element)]
        """
        return LightChain(map(handler, self))

    def filter(self, handler:FilterHandler) -> 'LightChain[Any]':
        """
        LightChain[element if handler(element)]
        """
        return LightChain(filter(handler, self))

    def reduce(self, handler:ReduceHandler, initializer:Any|None=None) -> T:
        """
        functools.reduce(handler, LightChain, initializer = LightChain.pop(0))
        """
        it = iter(self)
        return reduce(handler, it, initializer if initializer != None else next(it))
