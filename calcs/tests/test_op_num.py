import pytest
import calcs
from calcs import OperatorInfo, Var
from calcs.op_num import *
from sympy import Integer, Rational

adv_parser = calcs.give_advanced_parser(additional_prefix = [
	OperatorInfo(RealOperator, 'real'),
	OperatorInfo(ImagOperator, 'imag'),
	OperatorInfo(IncrementOperator, '++'),
	OperatorInfo(DecrementOperator, '--'),
], additional_postfix = [
	OperatorInfo(PostIncrementOperator, '++'),
	OperatorInfo(PostDecrementOperator, '--'),
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

def test_abs():
	n = adv_parser.parse("abs-42").eval({})
	assert n.value == 42

def test_pow():
	n = adv_parser.parse("3**2").eval({})
	assert n.value == 9

def test_factorial():
	n = adv_parser.parse("6!").eval({})
	assert n.value == 720

def test_real():
	n = adv_parser.parse("real (42+3.14i)").eval({})
	assert n.value == 42

def test_imag():
	n = adv_parser.parse("imag (42+3.14i)").eval({})
	assert n.value == Rational("3.14")

def test_inc(x, mapping):
	n = adv_parser.parse("++x").eval(mapping)
	assert n.is_lvalue
	assert n.var == x
	assert n.value == 43

def test_dec(x, mapping):
	n = adv_parser.parse("--x").eval(mapping)
	assert n.is_lvalue
	assert n.var == x
	assert n.value == 41

def test_inc(x, mapping):
	n = adv_parser.parse("x++").eval(mapping)
	assert not n.is_lvalue
	assert n.value == 42
	assert mapping[x].value == 43

def test_dec(x, mapping):
	n = adv_parser.parse("x--").eval(mapping)
	assert not n.is_lvalue
	assert n.value == 42
	assert mapping[x].value == 41
