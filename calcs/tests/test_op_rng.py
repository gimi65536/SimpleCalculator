import pytest
import calcs
from calcs import LValue, OperatorInfo, Var
from calcs.op_rng import *
from sympy import I, Integer, Rational

adv_parser = calcs.give_advanced_parser(additional_prefix = [
	OperatorInfo(calcs.op_num.RealOperator, 'real'),
	OperatorInfo(calcs.op_num.ImagOperator, 'imag'),
	OperatorInfo(SetSeedOperator, 'seed'),
	OperatorInfo(RandomIntOperator, 'rint'),
	OperatorInfo(RandomRealOperator, 'rreal'),
	OperatorInfo(RandomComplexOperator, 'rcomp'),
	OperatorInfo(RandomRangeZeroOperator, 'randrange'),
	OperatorInfo(RandomRangeStepOneOperator, 'randrange'),
	OperatorInfo(RandomRangeOperator, 'randrange'),
])

@pytest.fixture
def x():
	return Var('x')

@pytest.fixture
def mapping(x):
	return {x: LValue(x, calcs.NumberConstant(Integer(0)))}

def test_random():
	n = adv_parser.parse("random()").eval({})
	assert n.value >= 0
	assert n.value <= 1

def test_random_seed():
	n = adv_parser.parse("random 42").eval({})
	n2 = adv_parser.parse("random 42").eval({})
	assert n.value == n2.value

def test_random_dummy_seed(mapping):
	adv_parser.parse("x = _").eval(mapping)
	n = adv_parser.parse("random x").eval(mapping)
	n2 = adv_parser.parse("random ()").eval({})

	adv_parser.parse("random x").eval(mapping)
	n3 = adv_parser.parse("random _").eval({})
	# n == n2 in a very rarely probability
	assert (n.value == n2.value) or (n2.value == n3.value)

def test_seed():
	n = adv_parser.parse("random 42").eval({})
	adv_parser.parse("seed 42").eval({})
	n2 = adv_parser.parse("random()").eval({})
	assert n.value == n2.value

def test_randrange_unary():
	n = adv_parser.parse("randrange 10").eval({})
	assert n.value >= 0
	assert n.value <= 10

def test_randrange_binary():
	n = adv_parser.parse("randrange (-3.14, 3.14)").eval({})
	assert n.value >= -3
	assert n.value <= 3

def test_randrange_ternary():
	n = adv_parser.parse("randrange (-2.5-2i, 7.5+2i, 2.5+i)").eval({})
	assert (
		n.value == Rational("-2.5") - 2 * I or
		n.value == -I or
		n.value == Rational("2.5") or
		n.value == Rational("5") + I or
		n.value == Rational("7.5") + 2 * I
	)

def test_rint_basic():
	n = adv_parser.parse("rint (1, 10)").eval({})
	assert n.value >= 1
	assert n.value <= 10

def test_rint_rational():
	n = adv_parser.parse("rint (1.5, 2.5)").eval({})
	assert n.value == 2

def test_rint_reverse():
	n = adv_parser.parse("rint (2.5, 1.5)").eval({})
	assert n.value == 2

def test_rint_narrow():
	with pytest.raises(ValueError):
		n = adv_parser.parse("rint (1.1, 1.9)").eval({})

def test_rreal_basic():
	n = adv_parser.parse("rreal (1, 3.14)").eval({})
	assert n.value >= 1
	assert n.value <= Rational("3.14")

def test_rreal_reverse():
	n = adv_parser.parse("rreal (3.14, 1)").eval({})
	assert n.value >= 1
	assert n.value <= Rational("3.14")

def test_rcomp_basic(mapping):
	adv_parser.parse("x = rcomp (41, 43, -1, 1)").eval(mapping)
	r = adv_parser.parse("real x").eval(mapping)
	i = adv_parser.parse("imag x").eval(mapping)

	assert r.value >= 41
	assert r.value <= 43
	assert i.value >= -1
	assert i.value <= 1

def test_rcomp_reverse(mapping):
	adv_parser.parse("x = rcomp (43, 41, 1, -1)").eval(mapping)
	r = adv_parser.parse("real x").eval(mapping)
	i = adv_parser.parse("imag x").eval(mapping)

	assert r.value >= 41
	assert r.value <= 43
	assert i.value >= -1
	assert i.value <= 1
