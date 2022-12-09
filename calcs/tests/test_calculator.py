import pytest
import calcs
from sympy import Integer

parser = calcs.give_basic_parser()

def test_42():
	const = parser.parse("42")
	assert const.is_number
	assert const.value == Integer(42)
