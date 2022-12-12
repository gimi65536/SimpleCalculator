import pytest
import calcs
from calcs import LValue, OperatorInfo, Var
from calcs.op_basic import *
from sympy import I, Integer, Rational, S

parser = calcs.give_basic_parser()

class TestPlus:
	def test_real(self):
		n = parser.parse("3.14 + 42").eval({})
		assert n.is_number
		assert n.value == Rational("45.14")

	def test_complex(self):
		n = parser.parse("(1+2i) + (3+4j)").eval({})
		assert n.is_number
		assert n.value == Integer(4) + I * 6

	def test_bool_false(self):
		n = parser.parse("false + false").eval({})
		assert n.is_bool
		assert n.value == False

	def test_bool_ft(self):
		n = parser.parse("false + true").eval({})
		assert n.is_bool
		assert n.value == True

	def test_bool_tf(self):
		n = parser.parse("true + false").eval({})
		assert n.is_bool
		assert n.value == True

	def test_bool_true(self):
		n = parser.parse("true + true").eval({})
		assert n.is_bool
		assert n.value == True

	def test_string(self):
		n = parser.parse("'foo' + 'bar'").eval({})
		assert n.is_str
		assert n.value == "foobar"

class TestMinus:
	def test_real(self):
		n = parser.parse("3.14 - 42").eval({})
		assert n.is_number
		assert n.value == Rational("-38.86")

	def test_complex(self):
		n = parser.parse("(3+4i) - (1+2j)").eval({})
		assert n.is_number
		assert n.value == Integer(2) + I * 2

	def test_complex_to_real(self):
		n = parser.parse("(5+i) - (2+i)").eval({})
		assert n.is_number
		assert n.value == 3

	def test_bool_false(self):
		n = parser.parse("false - false").eval({})
		assert n.is_bool
		assert n.value == False

	def test_bool_ft(self):
		n = parser.parse("false - true").eval({})
		assert n.is_bool
		assert n.value == False

	def test_bool_tf(self):
		n = parser.parse("true - false").eval({})
		assert n.is_bool
		assert n.value == True

	def test_bool_true(self):
		n = parser.parse("true - true").eval({})
		assert n.is_bool
		assert n.value == False

class TestMultiple:
	def test_real(self):
		n = parser.parse("3.14 * 42").eval({})
		assert n.is_number
		assert n.value == Rational("131.88")

	def test_complex(self):
		n = parser.parse("(3+4i) * (1+2j)").eval({})
		assert n.is_number
		assert n.simplify().value == Integer(-5) + I * 10

	def test_complex_to_real(self):
		n = parser.parse("i*i").eval({})
		assert n.is_number
		assert n.value == -1

	def test_bool_false(self):
		n = parser.parse("false * false").eval({})
		assert n.is_bool
		assert n.value == False

	def test_bool_ft(self):
		n = parser.parse("false * true").eval({})
		assert n.is_bool
		assert n.value == False

	def test_bool_tf(self):
		n = parser.parse("true * false").eval({})
		assert n.is_bool
		assert n.value == False

	def test_bool_true(self):
		n = parser.parse("true * true").eval({})
		assert n.is_bool
		assert n.value == True

	def test_true_number(self):
		n = parser.parse("true * 42").eval({})
		assert n.is_number
		assert n.value == 42

	def test_false_number(self):
		n = parser.parse("false * 42").eval({})
		assert n.is_number
		assert n.value == 0

	def test_number_str(self):
		n = parser.parse("3 * 'foo'").eval({})
		assert n.is_str
		assert n.value == "foofoofoo"

	def test_true_str(self):
		n = parser.parse("true * 'foo'").eval({})
		assert n.is_str
		assert n.value == "foo"

	def test_false_str(self):
		n = parser.parse("false * 'foo'").eval({})
		assert n.is_str
		assert n.value == ""

	def test_minus_str(self):
		with pytest.raises(ValueError):
			n = parser.parse("-1 * 'foo'").eval({})

	def test_nonint_str(self):
		with pytest.raises(ValueError):
			n = parser.parse("3.14 * 'foo'").eval({})

class TestDivide:
	def test_real(self):
		n = parser.parse("3.14 / 42").eval({})
		assert n.is_number
		assert n.value == Rational(157, 2100)

	def test_complex(self):
		n = parser.parse("(3+4i) / (1+2j)").eval({})
		assert n.is_number
		assert n.simplify().value == Rational("2.2") - I * Rational("0.4")

	def test_complex_to_real(self):
		n = parser.parse("(10+4i) / (2.5+i)").eval({})
		assert n.is_number
		assert n.simplify().value == 4

class TestIntDivide:
	def test_real(self):
		n = parser.parse("3.14 // 42").eval({})
		assert n.is_number
		assert n.value == 0

	def test_complex(self):
		n = parser.parse("(3+4i) // (1+2j)").eval({})
		assert n.is_number
		assert n.value == Integer(2) - I

	def test_complex_to_real(self):
		n = parser.parse("(4.5+4.5i) // (1+i)").eval({})
		assert n.is_number
		assert n.value == 4

class TestModulo:
	def test_real(self):
		n = parser.parse("53.14 % 42").eval({})
		assert n.is_number
		assert n.value == Rational("11.14")

	@pytest.mark.skip(reason = "SymPy has had no way to handle this yet")
	def test_complex(self):
		n = parser.parse("(3+4i) % (1+2j)").eval({})
		assert n.is_number
		assert n.simplify().value == S("(3+4*I) - (1+2*I) * ((3+4*I) // (1+2*I))").simplify()

	def test_complex_to_real(self):
		n = parser.parse("(10+4i) % (2.5+i)").eval({})
		assert n.is_number
		assert n.value == 0

class TestPositive:
	def test_real(self):
		n = parser.parse("+3.14").eval({})
		assert n.is_number
		assert n.value == Rational("3.14")

	def test_complex(self):
		n = parser.parse("+(3+4j)").eval({})
		assert n.is_number
		assert n.value == Integer(3) + I * 4

class TestNegative:
	def test_real(self):
		n = parser.parse("-3.14").eval({})
		assert n.is_number
		assert n.value == Rational("-3.14")

	def test_complex(self):
		n = parser.parse("-(3+4j)").eval({})
		assert n.is_number
		assert n.value == Integer(-3) - I * 4

class TestNot:
	def test_true(self):
		n = parser.parse("~true").eval({})
		assert n.is_bool
		assert n.value is False

	def test_false(self):
		n = parser.parse("~false").eval({})
		assert n.is_bool
		assert n.value is True

	def test_zero(self):
		n = parser.parse("~0").eval({})
		assert n.is_bool
		assert n.value is True

	def test_one(self):
		n = parser.parse("~1").eval({})
		assert n.is_bool
		assert n.value is False

	def test_empty(self):
		n = parser.parse("~''").eval({})
		assert n.is_bool
		assert n.value is True

	def test_str(self):
		n = parser.parse("~'false'").eval({})
		assert n.is_bool
		assert n.value is False

@pytest.fixture
def x():
	return Var('x')

@pytest.fixture
def xvalue():
	return calcs.NumberConstant(Integer(42))

@pytest.fixture
def mapping(x, xvalue):
	return {x: LValue(x, xvalue)}

class TestLogic:
	parser = calcs.Parser(
		ptable = [calcs.PrecedenceLayer.right_asso(OperatorInfo(calcs.op_assign.AssignOperator, '='))],
		prefix_ops = [
			OperatorInfo(AndOperator, 'and'),
			OperatorInfo(OrOperator, 'or'),
			OperatorInfo(ImplOperator, 'impl'),
			OperatorInfo(NimplOperator, 'nimpl'),
			OperatorInfo(XorOperator, 'xor'),
			OperatorInfo(IffOperator, 'iff'),
			OperatorInfo(NandOperator, 'nand'),
			OperatorInfo(NorOperator, 'nor'),
			OperatorInfo(ConverseImplOperator, 'cimpl'),
			OperatorInfo(ConverseNimplOperator, 'cnimpl'),
	])

	def _test(self, op, TT, TF, FT, FF):
		n = self.parser.parse(f"{op}(true, true)").eval({})
		assert n.is_bool
		assert n.value is TT

		n = self.parser.parse(f"{op}(true, false)").eval({})
		assert n.is_bool
		assert n.value is TF

		n = self.parser.parse(f"{op}(false, true)").eval({})
		assert n.is_bool
		assert n.value is FT

		n = self.parser.parse(f"{op}(false, false)").eval({})
		assert n.is_bool
		assert n.value is FF

	def test_and(self):
		op = "and"
		TT, TF = True, False
		FT, FF = False, False
		self._test(op, TT, TF, FT, FF)

	def test_or(self):
		op = "or"
		TT, TF = True, True
		FT, FF = True, False
		self._test(op, TT, TF, FT, FF)

	def test_impl(self):
		op = "impl"
		TT, TF = True, False
		FT, FF = True, True
		self._test(op, TT, TF, FT, FF)

	def test_nimpl(self):
		op = "nimpl"
		TT, TF = False, True
		FT, FF = False, False
		self._test(op, TT, TF, FT, FF)

	def test_xor(self):
		op = "xor"
		TT, TF = False, True
		FT, FF = True, False
		self._test(op, TT, TF, FT, FF)

	def test_iff(self):
		op = "iff"
		TT, TF = True, False
		FT, FF = False, True
		self._test(op, TT, TF, FT, FF)

	def test_nand(self):
		op = "nand"
		TT, TF = False, True
		FT, FF = True, True
		self._test(op, TT, TF, FT, FF)

	def test_nor(self):
		op = "nor"
		TT, TF = False, False
		FT, FF = False, True
		self._test(op, TT, TF, FT, FF)

	def test_cimpl(self):
		op = "cimpl"
		TT, TF = True, True
		FT, FF = False, True
		self._test(op, TT, TF, FT, FF)

	def test_cnimpl(self):
		op = "cnimpl"
		TT, TF = False, False
		FT, FF = True, False
		self._test(op, TT, TF, FT, FF)

	def test_shortcut_and_1(self, x, mapping):
		n = self.parser.parse("and(x = 5, x = 0)").eval(mapping)
		assert mapping[x].value == 0
		assert n.value is False

	def test_shortcut_and_2(self, x, mapping):
		n = self.parser.parse("and(x = 0, x = 5)").eval(mapping)
		assert mapping[x].value == 0
		assert n.value is False

	def test_shortcut_or_1(self, x, mapping):
		n = self.parser.parse("or(x = 0, x = 5)").eval(mapping)
		assert mapping[x].value == 5
		assert n.value is True

	def test_shortcut_or_2(self, x, mapping):
		n = self.parser.parse("or(x = 5, x = 0)").eval(mapping)
		assert mapping[x].value == 5
		assert n.value is True

	def test_shortcut_notb_1(self, x, mapping): # a and not b
		n = self.parser.parse("nimpl(x = 5, x = 0)").eval(mapping)
		assert mapping[x].value == 0
		assert n.value is True

	def test_shortcut_notb_2(self, x, mapping): # a and not b
		n = self.parser.parse("nimpl(x = 0, x = 5)").eval(mapping)
		assert mapping[x].value == 0
		assert n.value is False

class TestCompare:
	def test_eq(self):
		n = parser.parse("(10+4i)/(2.5+i) == 4").eval({})
		assert n.is_bool
		assert n.value is True

	def test_ne(self):
		n = parser.parse("(10+4i)/(2.5+i) != 4").eval({})
		assert n.is_bool
		assert n.value is False

	def test_g(self):
		n = parser.parse("(10+4i)/(2.5+i) > 4").eval({})
		assert n.is_bool
		assert n.value is False

	def test_ge(self):
		n = parser.parse("(10+4i)/(2.5+i) >= 4").eval({})
		assert n.is_bool
		assert n.value is True

	def test_l(self):
		n = parser.parse("(10+4i)/(2.5+i) < 4").eval({})
		assert n.is_bool
		assert n.value is False

	def test_le(self):
		n = parser.parse("(10+4i)/(2.5+i) <= 4").eval({})
		assert n.is_bool
		assert n.value is True

	def test_complex(self):
		n = parser.parse("(1 < I) || (1 == I) || (1 > I)").eval({})
		assert n.is_bool
		assert n.value is False

	def test_between_complex(self):
		# Any of >, >=, <, <= cannot be applied on complex numbers in SymPy
		# But we allow >= <= to be applied since "=" is there...
		n = parser.parse("I >= I").eval({})
		assert n.is_bool
		assert n.value is True
