import pytest
import calcs

adv_parser = calcs.give_advanced_parser()

def test_len():
	n = adv_parser.parse("len 'foo bar'").eval({})
	assert n.is_number
	assert n.value == 7

def test_parse():
	n = adv_parser.parse("parse 'sin(pi)tan(42)'").eval({})
	assert n.is_number
	assert n.value == 0

def test_parse_bool():
	n = adv_parser.parse("parse 'true'").eval({})
	assert n.is_bool
	assert n.value is True

def test_parse_rel():
	n = adv_parser.parse("parse 'sin(pi) < cos(pi)'").eval({})
	assert n.is_bool
	assert n.value is False

def test_parse_eq():
	n = adv_parser.parse("parse '4*(5/2 - I)*(10 + 4*I)/29 = 4'").eval({})
	assert n.is_bool
	assert n.value is True

def test_parse_exactly():
	n = adv_parser.parse("parse '4*(5/2 - I)*(10 + 4*I)/29 == 4'").eval({})
	assert n.is_bool
	assert n.value is False
