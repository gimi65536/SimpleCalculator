import pytest
import calcs
from sympy import Integer, Rational

parser = calcs.give_basic_parser()

def test_42():
	const = parser.parse("42")
	assert const.is_number
	assert const.value == Integer(42)

def test_00042():
	const = parser.parse("00042")
	assert const.is_number
	assert const.value == Integer(42)

def test_3p14():
	const = parser.parse("3.14")
	assert const.is_number
	assert const.value == Rational("3.14")

def test_0003p14():
	const = parser.parse("0003.14")
	assert const.is_number
	assert const.value == Rational("3.14")

def test_p14():
	with pytest.raises(calcs.exceptions.ParseError):
		const = parser.parse(".14")
