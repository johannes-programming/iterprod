__all__: list[str] = ["iterprod"]


from collections.abc import Generator, Iterable, Sequence
from typing import Any, SupportsIndex, TypeVar

Item = TypeVar("Item")


def get_total_and_infos(
    *iterables: Iterable[Item],
    repeat: SupportsIndex = 1,
) -> tuple[int, Sequence[tuple[int, tuple[Item, ...]]]]:
    div: int
    infos: list[Any]
    pools: list[Any]
    pools = list(map(tuple, iterables))
    pools *= repeat
    div = 1
    infos = list()
    for pool in reversed(pools):
        infos.append((div, pool))
        div *= len(pool)
    return div, tuple(reversed(infos))


def iterprod(
    *iterables: Iterable[Item],
    repeat: SupportsIndex = 1,
) -> Generator[tuple[Item, ...], None, None]:
    "This generator iterates the Cartesian product of the given iterables."
    count: int
    infos: Sequence[tuple[int, tuple[Item, ...]]]
    total: int
    total, infos = get_total_and_infos(*iterables, repeat=repeat)
    for count in range(total):
        yield tuple(pool[count // div % len(pool)] for div, pool in infos)
