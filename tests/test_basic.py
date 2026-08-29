"""Demo tests for the workshop's three-phase-execution exercise.

Flip BREAK_ME_ON_PURPOSE to True to make the suite fail deliberately --
this is the intentional trigger for Phase B's "break something on purpose"
demo (Stage 3 debug rerun). Flip it back to False afterwards.
"""

import pytest

from ci_patterns_demo import greet

BREAK_ME_ON_PURPOSE = True


def test_greet_says_hello():
    assert greet("PyCon PL") == "Hello, PyCon PL!"


def test_greet_rejects_empty_name():
    with pytest.raises(ValueError):
        greet("")


def test_intentional_break_switch():
    if BREAK_ME_ON_PURPOSE:
        assert greet("workshop") == "this will never match on purpose"
