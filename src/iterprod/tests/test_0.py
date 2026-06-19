import enum
import functools
import itertools
import tomllib
import unittest
from collections.abc import Iterable
from importlib import resources
from typing import Any, Optional, Self, cast

from iterprod import core

__all__ = ["Test_0"]


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
        iterables: list[Iterable[Any]],
        solution: Any = None,
        **kwargs: Any,
    ) -> None:
        with self.assertRaises(Exception, msg="invalid"):
            list(core.iterprod(*iterables, **kwargs))

    def go_valid(
        self: Self,
        *,
        iterables: list[Iterable[Any]],
        parallel: bool,
        solution: Optional[list[list[Any]]] = None,
        **kwargs: Any,
    ) -> None:
        answer: list[tuple[Any, ...]]
        solution_: list[tuple[Any, ...]]
        answer = list(core.iterprod(*iterables, **kwargs))
        if parallel:
            solution_ = list(itertools.product(*iterables, **kwargs))
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
