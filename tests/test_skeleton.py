# -*- coding: utf-8 -*-

import pytest
from nflapi.skeleton import fib

__author__ = "Clifford Wollam"
__copyright__ = "Clifford Wollam"
__license__ = "gpl3"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
