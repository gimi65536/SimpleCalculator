import pytest
import calcs
from calcs import LValue, OperatorInfo, Var
from calcs.op_utils import *
from sympy import Integer, Rational

adv_parser = calcs.give_advanced_parser(additional_prefix = [
	OperatorInfo(ToStringOperator, 'to_str'),
	OperatorInfo(DedummizeOperator, 'dedummy'),
	OperatorInfo(RepeatTwiceOperator, 'repeat2'),
	OperatorInfo(RepeatTimesOperator, 'repeatN'),
])

@pytest.fixture
def x():
	return Var('x')

@pytest.fixture
def xvalue():
	return calcs.NumberConstant(Integer(42))

@pytest.fixture
def mapping(x, xvalue):
	return {x: LValue(x, xvalue)}

def test_to_str():
	n = adv_parser.parse("to_str (4*(5/2 - I)*(10 + 4*I)/29)").eval({})
	assert n.is_str
	assert n.value == "(10 - 4*I)*(10 + 4*I)/29" # Not fully expanded

def test_print_const():
	n = adv_parser.parse("print (4*(5/2 - I)*(10 + 4*I)/29)").eval({})
	assert n.is_str
	assert n.value == "4"

def test_pass(x, mapping):
	n = adv_parser.parse("pass (x = 0, true)").eval(mapping)
	assert n.is_bool
	assert n.value is True
	assert mapping[x].value == 0

def test_reverse():
	n = adv_parser.parse("reverse (3 / 42)").eval({})
	assert n.is_number
	assert n.value == Integer(42) / Integer(3)

def test_dummy():
	n = adv_parser.parse("dummy 42").eval({})
	assert n.is_number
	assert n.is_dummy
	assert n.value == 42

def test_dedummy():
	n = adv_parser.parse("dedummy (dummy 42)").eval({})
	assert n.is_number
	assert not n.is_dummy
	assert n.value == 42

def test_repeat2(x, mapping):
	n = adv_parser.parse("repeat2 (x = 2 * x)").eval(mapping)
	assert isinstance(n, LValue)
	assert n.content.is_number
	assert n.content.value == 42 * 4

def test_repeatN(x, mapping):
	n = adv_parser.parse("repeatN (10, x = 2 * x)").eval(mapping)
	assert isinstance(n, LValue)
	assert n.content.is_number
	assert n.content.value == 42 * (2 ** 10)

def test_raise():
	with pytest.raises(calcs.exceptions.UserDefinedError) as e:
		n = adv_parser.parse("raise 'Test Error'").eval({})
	assert e.value.msg == "Test Error"

def test_decimal():
	n = adv_parser.parse(".00114514").eval({})
	assert n.is_number
	assert n.value == Rational("0.114514")

def test_decimal_str():
	n = adv_parser.parse(". '00114514'").eval({})
	assert n.is_number
	assert n.value == Rational("0.00114514")

def test_decimal(mapping):
	n = adv_parser.parse(".x").eval(mapping)
	assert n.is_number
	assert n.value == Rational("0.42")

def test_move_var(mapping):
	n = adv_parser.parse("move(x)").eval(mapping)
	assert n.is_constant
	assert n.value == 42

def test_move_const(mapping):
	n = adv_parser.parse("move(1+1)").eval(mapping)
	assert n.is_constant
	assert n.value == 2
