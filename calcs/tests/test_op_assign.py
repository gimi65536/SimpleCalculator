import pytest
import calcs
from calcs import Var, LValue
from calcs.op_assign import *
from sympy import Integer, Rational

adv_parser = calcs.give_advanced_parser()

@pytest.fixture
def x():
	return Var('x')

@pytest.fixture
def y():
	return Var('y')

@pytest.fixture
def xvalue():
	return calcs.NumberConstant(Integer(42))

@pytest.fixture
def yvalue():
	return calcs.NumberConstant(Integer(114))

@pytest.fixture
def mapping(x, y, xvalue, yvalue):
	return {x: LValue(x, xvalue), y: LValue(y, yvalue)}

def test_assign(x, mapping):
	n = adv_parser.parse("x = 3.14").eval(mapping)
	assert n.is_lvalue
	assert n.var == x
	assert n.content.is_number
	assert n.value == Rational("3.14")
	assert mapping[x].value == Rational("3.14")

def test_assign_rvalue(mapping):
	with pytest.raises(ValueError):
		n = adv_parser.parse("1 + 1 = 2").eval(mapping)

def test_assign_var(x, y, yvalue, mapping):
	n = adv_parser.parse("x = y").eval(mapping)
	assert n.is_lvalue
	assert n.var == x
	assert n.content == yvalue
	assert mapping[x].content == yvalue
	assert mapping[y].content == yvalue
