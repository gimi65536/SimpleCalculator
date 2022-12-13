import pytest
import calcs
from calcs import LValue, Var
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

def test_assign_dummy(x, mapping):
	n = adv_parser.parse("x = _").eval(mapping)
	assert not n.content.is_dummy

def test_declare():
	mapping = {}
	n = adv_parser.parse("x := 42").eval(mapping)
	assert n.is_lvalue
	assert n.var.name == "x"
	assert n.var.scope is None
	assert mapping[n.var].value == 42

def test_redeclare():
	with pytest.raises(ValueError):
		n = adv_parser.parse("x := x := 42").eval({})

def test_ref(mapping):
	n = adv_parser.parse("z :=& x").eval(mapping)
	assert len(mapping) == 3
	assert n.is_lvalue
	assert n.var.name == "x"
	assert n.value == 42

def test_ref_assign(x, mapping):
	n = adv_parser.parse("pass(z :=& x, z = y.514)").eval(mapping)
	assert len(mapping) == 3
	assert n.is_lvalue
	assert n.var.name == "x"
	assert n.value == "114514"

def test_ref_redeclare(mapping):
	with pytest.raises(ValueError):
		n = adv_parser.parse("y :=& x").eval(mapping)
