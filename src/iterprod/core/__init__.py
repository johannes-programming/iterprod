import operator
from collections.abc import Generator, Iterable
from typing import Any, SupportsIndex

__all__ = ["iterprod"]


def iterprod(
    *iterables: Iterable[Any],
    repeat: SupportsIndex = 1,
) -> Generator[tuple[Any, ...], None, None]:
    indeces: list[int]
    lengths: tuple[int, ...]
    pools: list[tuple[Any, ...]]
    repeat_: int
    repeat_ = operator.index(repeat)
    if repeat_ < 0:
        raise ValueError("repeat argument cannot be negative")
    pools = list(map(tuple, iterables))
    if () in pools:
        return
    pools *= repeat_
    indeces = [0] * len(pools)
    lengths = tuple(map(len, pools))
    while True:
        yield tuple(map(operator.getitem, pools, indeces))
        try:
            incr(indeces, lengths)
        except IndexError:
            return


def incr(indeces: list[int], lengths: tuple[int, ...]) -> None:
    j: int
    indeces[-1] += 1
    j = -1
    while True:
        if indeces[j] < lengths[j]:
            return
        indeces[j] = 0
        indeces[j - 1] += 1
        j -= 1
