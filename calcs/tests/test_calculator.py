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

def test_true():
	const = parser.parse("true")
	assert const.is_bool
	assert const.value is True

def test_True():
	const = parser.parse("True")
	assert const.is_bool
	assert const.value is True

def test_TRUE():
	const = parser.parse("TRUE")
	assert const.is_bool
	assert const.value is True

def test_false():
	const = parser.parse("false")
	assert const.is_bool
	assert const.value is False

def test_False():
	const = parser.parse("False")
	assert const.is_bool
	assert const.value is False

def test_FALSE():
	const = parser.parse("FALSE")
	assert const.is_bool
	assert const.value is False

def test_string_sq():
	const = parser.parse(R"""'foo bar   42\'\"\\\1\a...++ "'""")
	assert const.is_str
	assert const.value == R'''foo bar   42'"\1a...++ "'''

def test_string_dq():
	const = parser.parse(R'''"foo bar   42\'\"\\\1\a...++ '"''')
	assert const.is_str
	assert const.value == R"""foo bar   42'"\1a...++ '"""
