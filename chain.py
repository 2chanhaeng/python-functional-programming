from typing import List, Iterable, TypeVar, Any, Callable, Optional, TypeAlias, Iterator, overload
from functools import reduce
from itertools import accumulate
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

    def reduce(self, handler:ReduceHandler, initial:T|None=None, start:int=0) -> T:
        """
        handler(one) => handler(previous)

        handler(one, two) => handler(previous, element)

        handler(one, two, tree) => handler(previous, element, index)

        handler(one, two, tree, four) => handler(previous, element, index, origin_Chain)
        
        handler(one, two, tree, four, *more) => handler(previous, element, index, origin_Chain, *([None] * len(more))
        """
        iterator = iter(self)
        is_init = 0
        if initial == None:
            initial = next(iterator)
            is_init = 1
        match len(getfullargspec(handler).args):
            case 1:
                return reduce(lambda initial, _: handler(initial), iterator, initial)
            case 2:
                return reduce(handler, iterator, initial)
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

    def filter(self, handler:FilterHandler, filter_true:bool=True) -> 'LightChain[Any]':
        """
        LightChain[element if handler(element)]

        LightChain[element if not handler(element)]
        """
        if filter_true:
            return LightChain(filter(handler, self))
        not_handler = lambda x: not handler(x)
        return LightChain(filter(not_handler, self))

    def reduce(self, handler:ReduceHandler, initial:Any|None=None) -> T:
        """
        functools.reduce(handler, LightChain, initial = LightChain.pop(0))
        """
        iterator = iter(self)
        return reduce(handler, iterator, initial if initial != None else next(iterator))

    def accumulate(self, handler:ReduceHandler, initial:Any|None=None) -> T:
        """
        LightChain[itertools.accumulate(LightChain, handler)]
        """
        return (
            LightChain(accumulate(self, handler))
            if initial == None
            else LightChain(accumulate(self, handler, initial = initial))[1:]
        )

    def append(self, __object:Any) -> 'LightChain':
        """
        LightChain[*origin_elements, new_element]
        """
        return LightChain(self + (__object,))

    def insert(self, __index:int, __object:Any) -> 'LightChain':
        """
        LightChain[origin_elements[:__index], new_element, origin_elements[__index:]]
        """
        return LightChain(self[:__index] + (__object,) + self[__index:])

    def pop(self, __index:int=None) -> 'LightChain["LightChain"[T],T]':
        """
        LightChain[LightChain_without_index_element, index_elment]
        """
        _list = list(self)
        popped = _list.pop(__index) if __index != None else _list.pop()
        return LightChain((LightChain(_list), popped))

    def replace(self, __1:int, __2:Any, __3:Any=..., __4:Any=...) -> 'LightChain':
        """
        LightChain[index] = new_element

        LightChain[start:end] = new_element OR new_elements 

        LightChain[start:end:step] = new_elements 
        """
        _list = list(self)
        if __3 == ...:
            _list[__1] = __2
            return LightChain(_list)
        if __4 == ...:
            _list[__1:__2] = __3
            return LightChain(_list)
        _list[__1:__2:__3] = __4
        return LightChain(_list)

    def remove(self, __1:int, __2:Any=..., __3:Any=...) -> 'LightChain':
        """
        LightChain[index_removed]

        LightChain[strat_to_end_removed]

        LightChain[strat_to_end_by_step_removed]
        """
        if __2 == ...:
            return self.replace(__1, [])
        if __3 == ...:
            return self.replace(__1, __2, [])
        return self.replace(__1, __2, __3, [])
    
    def copy(self) -> 'LightChain':
        """
        LightChain[origin]
        """
        return LightChain(self)

    def extend(self, other:Iterable) -> 'LightChain':
        """
        LightChain[*origin_elements, *new_elements]
        """
        return self + LightChain(other)

    def reverse(self) -> 'LightChain':
        """
        LightChain[::-1]
        """
        return LightChain(self[::-1])

    @staticmethod
    def __search(iterator:Iterator, __handler:Callable[[Any], bool], __index:int=0) -> int:
        popped = next(iterator, ...)
        if popped == ...:
            return -1
        if __handler(popped):
            return __index
        return LightChain.__search(iterator, __handler, __index + 1)

    def find(self, __object:Any) -> int:
        return LightChain.__search(iter(self), lambda x: x == __object)

    def search(self, __handler:Callable[[Any], bool]) -> int:
        return LightChain.__search(iter(self), __handler)