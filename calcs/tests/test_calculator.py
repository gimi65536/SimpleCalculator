import pytest
import calcs
from sympy import I, Integer, Rational, zoo

parser = calcs.give_basic_parser()

adv_parser = calcs.give_advanced_parser()

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
		const = parser.parse("3.14j")
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

	def test_dummy(self):
		const = parser.parse("_")
		assert const.is_number
		assert const.is_dummy

	def test_complicated_expr(self):
		const = parser.parse("4*(5/2 - I)*(10 + 4*I)/29").eval({})
		assert const.value != 4 # Cannot be implicitly simplified to 4
		str_const = const.to_str() # But to_str should do simplification
		assert str_const.value == "4"

class TestParser:
	def test_minus2(self):
		n = parser.parse("3--5").eval({})
		assert n.value == 8

	def test_minus2(self):
		n = parser.parse("3---5").eval({})
		assert n.value == -2

	def test_minus2(self):
		n = parser.parse("3----5").eval({})
		assert n.value == 8

	def test_point_space_1(self):
		n = parser.parse("0 .5").eval({})
		assert n.value == "05"

	def test_point_space_2(self):
		n = parser.parse("0. 5").eval({})
		assert n.value == "05"

	def test_point_space_3(self):
		n = parser.parse("0.5.6").eval({})
		assert n.value == "0.56"

	def test_point_space_4(self):
		n = parser.parse("0. 5.6").eval({})
		assert n.value == "05.6"

	def test_incorrect_quote_1(self):
		with pytest.raises(calcs.exceptions.TokenizeError):
			n = parser.parse(R"""'123""")

	def test_incorrect_quote_2(self):
		with pytest.raises(calcs.exceptions.TokenizeError):
			n = parser.parse(R'''"123''')

	def test_incorrect_symbol(self):
		with pytest.raises(calcs.exceptions.TokenizeError):
			n = parser.parse("123@456")

	def test_varname_1(self):
		var = parser.parse("var")
		assert isinstance(var, calcs.Var)
		assert var.name == "var"

	def test_varname_2(self):
		var = parser.parse("000var")
		assert isinstance(var, calcs.Var)
		assert var.name == "000var"

	def test_word_unary(self):
		n = adv_parser.parse("abs-42").eval({})
		assert n.value == 42

	def test_nullary(self):
		n = adv_parser.parse("random ()").eval({})
		assert n.is_number
		assert n.value >= 0
		assert n.value <= 1

	def test_overload(self):
		n = adv_parser.parse("random 42").eval({})
		assert n.is_number
		assert n.value >= 0
		assert n.value <= 1

	def test_tail_comma(self):
		n = adv_parser.parse("len ('foo', )").eval({})
		assert n.is_number
		assert n.value == 3

	def test_prefix_binary(self):
		n = adv_parser.parse("pass ('foo', 'bar')").eval({})
		assert n.is_str
		assert n.value == "bar"

	def test_wrong_ary_1(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = adv_parser.parse("random")

	def test_wrong_ary_2(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = adv_parser.parse("random (114, 514)")

	def test_lonely_prefix(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("~")

	def test_lonely_postfix(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("!")

	def test_lonely_infix(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("*")

	def test_single_infix_1(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("5*")

	def test_single_infix_2(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("*5")

	def test_single_comma(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = adv_parser.parse("pass (, 42)")

	def test_error_tuple_1(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = adv_parser.parse("pass (('foo', 'bar'), 42)")

	def test_error_tuple_2(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = adv_parser.parse("pass (42, ('foo', 'bar'))")

	def test_wait_literal_but_special(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("3+,")

	def test_wait_literal_but_infix(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("3+*")

	def test_wait_literal_but_postfix(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("3+!")

	def test_unclosed_parenthesis(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("42)")

	def test_comma_outsides_parenthesis(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("foo, bar")

	def test_wait_infix_but_special(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("foo(42)")

	def test_wait_infix_but_prefix(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("'foo' ~ 'bar'")

	def test_wait_infix_but_word(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("foo bar")

	def test_empty(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("")

	def test_redundant_operator(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("3*")

	def test_topmost_tuple(self):
		with pytest.raises(calcs.exceptions.ParseError):
			n = parser.parse("(foo, bar)")

class TestPrecedence:
	def test_prefix_1(self):
		n = parser.parse("~+0").eval({})
		assert n.is_bool
		assert n.value is True

	def test_prefix_2(self):
		with pytest.raises(ValueError):
			n = parser.parse("+~0").eval({})

	def test_postfix(self):
		# The default parser has only one postfix operator...
		NotImplemented

	def test_infix_1(self):
		n = parser.parse("3 + 5 * 6").eval({})
		assert n.value != 48
		assert n.value == 33

	def test_infix_2(self):
		n = parser.parse("(3 + 5) * 6").eval({})
		assert n.value == 48
		assert n.value != 33

	def test_left_1(self):
		n = parser.parse("3 + 2 . 5").eval({})
		assert n.value == "55"

	def test_left_2(self):
		n = parser.parse("3 . 2 + 5").eval({})
		assert n.value == "325"		

	def test_right(self):
		n = parser.parse("3 ** 3 ** 3").eval({})
		assert n.value == 3 ** 27
		assert n.value != 27 ** 3

	def test_pre_in_1(self):
		n = parser.parse("~3 * 5").eval({})
		assert n.value == 0

	def test_pre_in_2(self):
		n = parser.parse("~(3 * 5)").eval({})
		assert n.value is False

	def test_post_in_1(self):
		n = parser.parse("3 * 2!").eval({})
		assert n.value == 6

	def test_post_in_2(self):
		n = parser.parse("(3 * 2)!").eval({})
		assert n.value == 720

	def test_pre_post_1(self):
		with pytest.raises(ValueError):
			n = adv_parser.parse("!3!").eval({})

	def test_pre_post_2(self):
		n = adv_parser.parse("!(3!)").eval({})
		assert n.value is False

	def test_pre_post_in(self):
		n = parser.parse("-3 * 4!").eval({})
		assert n.value == -72
		assert n.value != -479001600 # -(12!)
		assert n.value != zoo # (-12)!
