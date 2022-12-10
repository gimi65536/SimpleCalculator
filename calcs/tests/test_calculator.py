import pytest
import calcs
from sympy import I, Integer, Rational

parser = calcs.give_basic_parser()

class TestConst:
	def test_42(self):
		const = parser.parse("42")
		assert const.is_number
		assert const.value == Integer(42)

	def test_00042(self):
		const = parser.parse("00042")
		assert const.is_number
		assert const.value == Integer(42)

	def test_3p14(self):
		const = parser.parse("3.14")
		assert const.is_number
		assert const.value == Rational("3.14")

	def test_0003p14(self):
		const = parser.parse("0003.14")
		assert const.is_number
		assert const.value == Rational("3.14")

	def test_p14(self):
		with pytest.raises(calcs.exceptions.ParseError):
			const = parser.parse(".14")

	def test_i(self):
		const = parser.parse("i")
		assert const.is_number
		assert const.value == I

	def test_I(self):
		const = parser.parse("I")
		assert const.is_number
		assert const.value == I

	def test_j(self):
		const = parser.parse("j")
		assert const.is_number
		assert const.value == I

	def test_J(self):
		const = parser.parse("J")
		assert const.is_number
		assert const.value == I

	def test_42i(self):
		const = parser.parse("42i")
		assert const.is_number
		assert const.value == I * 42

	def test_3p14j(self):
		const = parser.parse("3.14i")
		assert const.is_number
		assert const.value == I * Rational("3.14")

	def test_true(self):
		const = parser.parse("true")
		assert const.is_bool
		assert const.value is True

	def test_True(self):
		const = parser.parse("True")
		assert const.is_bool
		assert const.value is True

	def test_TRUE(self):
		const = parser.parse("TRUE")
		assert const.is_bool
		assert const.value is True

	def test_false(self):
		const = parser.parse("false")
		assert const.is_bool
		assert const.value is False

	def test_False(self):
		const = parser.parse("False")
		assert const.is_bool
		assert const.value is False

	def test_FALSE(self):
		const = parser.parse("FALSE")
		assert const.is_bool
		assert const.value is False

	def test_string_sq(self):
		const = parser.parse(R"""'foo bar   42\'\"\\\1\a...++ "'""")
		assert const.is_str
		assert const.value == R'''foo bar   42'"\1a...++ "'''

	def test_string_dq(self):
		const = parser.parse(R'''"foo bar   42\'\"\\\1\a...++ '"''')
		assert const.is_str
		assert const.value == R"""foo bar   42'"\1a...++ '"""
