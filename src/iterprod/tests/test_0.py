__all__: list[str] = ["Test_0"]


import enum
import functools
import itertools
import math
import tomllib
import unittest
from collections import abc
from importlib import resources
from typing import Any, Optional, Self, cast

from iterprod import core


class Util(enum.Enum):
    util = None

    @functools.cached_property
    def data(self: Self) -> dict[str, Any]:
        text: str
        text = resources.read_text("iterprod.tests", "testdata.toml")
        return tomllib.loads(text)

    @functools.cached_property
    def go(self: Self) -> dict[str, dict[str, Any]]:
        return cast(dict[str, dict[str, Any]], Util.util.data["go"])


class Test_0(unittest.TestCase):
    def go(
        self: Self,
        name: str,
        /,
        *,
        valid: bool,
        **kwargs: Any,
    ) -> None:
        with self.subTest(msg="go %r" % name):
            if valid:
                self.go_valid(**kwargs)
            else:
                self.go_invalid(**kwargs)

    def go_invalid(
        self: Self,
        /,
        *,
        iterables: list[abc.Sequence[Any]],
        repeat: Any = None,
        **kwargs: Any,
    ) -> None:
        kwargs_: dict[str, Any]
        kwargs_ = dict()
        if repeat is not None:
            kwargs_["repeat"] = repeat
        with self.assertRaises(Exception, msg="invalid"):
            list(core.iterprod(*iterables, **kwargs_))

    def go_valid(
        self: Self,
        *,
        iterables: list[abc.Sequence[Any]],
        parallel: bool,
        repeat: Any = None,
        solution: Optional[list[list[Any]]] = None,
    ) -> None:
        answer: list[tuple[Any, ...]]
        answer_len: int
        item_len: int
        solution_: list[tuple[Any, ...]]
        kwargs_: dict[str, Any] = {}
        if repeat is not None:
            kwargs_["repeat"] = repeat
        answer = list(core.iterprod(*iterables, **kwargs_))
        if repeat is None:
            answer_len = 1
        else:
            answer_len = max(0, repeat)
        answer_len = math.prod(map(len, iterables)) ** answer_len
        self.assertEqual(len(answer), answer_len)
        item_len = len(iterables)
        if repeat is not None:
            item_len *= max(0, repeat)
        self.assertLessEqual(set(map(len, answer)), {item_len})
        if parallel:
            solution_ = list(itertools.product(*iterables, **kwargs_))
            self.assertEqual(
                answer,
                solution_,
                msg="iterprod",
            )
        if solution is not None:
            solution_ = list(map(tuple, solution))
            self.assertEqual(
                answer,
                solution_,
                msg="testdata",
            )

    def test_0(self: Self) -> None:
        n: str
        q: dict[str, Any]
        for n, q in Util.util.go.items():
            self.go(n, **q)


if __name__ == "__main__":
    unittest.main()
