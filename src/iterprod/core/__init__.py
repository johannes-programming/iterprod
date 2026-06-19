import operator
from collections.abc import Generator, Iterable
from typing import SupportsIndex, TypeVar

__all__ = ["iterprod"]

Item = TypeVar("Item")


def incr(
    indeces: list[int],
    lengths: tuple[int, ...],
) -> None:
    j: int
    indeces[-1] += 1
    j = -1
    while True:
        if indeces[j] < lengths[j]:
            return
        indeces[j] = 0
        j -= 1
        indeces[j] += 1


def iterprod(
    *iterables: Iterable[Item],
    repeat: SupportsIndex = 1,
) -> Generator[tuple[Item, ...], None, None]:
    "This generator iterates the Cartesian product of the given iterables."
    indeces: list[int]
    lengths: tuple[int, ...]
    pools: list[tuple[Item, ...]]
    repeat_: int
    repeat_ = operator.index(repeat)
    pools = list(map(tuple, iterables))
    if () in pools:
        return
    pools *= abs(repeat_)
    if repeat_ < 0:
        pools.reverse()
    indeces = [0] * len(pools)
    lengths = tuple(map(len, pools))
    while True:
        yield tuple(map(operator.getitem, pools, indeces))
        try:
            incr(indeces, lengths)
        except IndexError:
            break
