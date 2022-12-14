from .calculator import (
	Associability,
	OperatorInfo,
	Parser,
	PrecedenceLayer
)
from .ops import *
from .types import *
from . import (
	op_assign,
	op_basic,
	op_num,
	op_rng,
	op_str,
	op_utils
)

def give_basic_parser():
	default_precedence_table = {
		9: PrecedenceLayer.right_asso(
			OperatorInfo(op_num.PowOperator, '**')
		),
		10: PrecedenceLayer.left_asso(
			OperatorInfo(op_basic.MultipleOperator, '*'),
			OperatorInfo(op_basic.DivideOperator, '/'),
			OperatorInfo(op_basic.IntegerDivideOperator, '//'),
			OperatorInfo(op_basic.ModuloOperator, '%'),
		),
		20: PrecedenceLayer.left_asso(
			OperatorInfo(op_basic.PlusOperator, '+'),
			OperatorInfo(op_basic.MinusOperator, '-'),
			OperatorInfo(op_basic.ConcatOperator, '.'),
		),
		70: PrecedenceLayer.left_asso(
			OperatorInfo(op_basic.LessOperator, '<'),
			OperatorInfo(op_basic.LeOperator, '<='),
			OperatorInfo(op_basic.GreaterOperator, '>'),
			OperatorInfo(op_basic.GeOperator, '>='),
		),
		80: PrecedenceLayer.left_asso(
			OperatorInfo(op_basic.EqualOperator, '=='),
			OperatorInfo(op_basic.NonequalOperator, '!='),
		),
		110: PrecedenceLayer.right_asso(
			OperatorInfo(op_basic.AndOperator, '&&'),
			OperatorInfo(op_basic.OrOperator, '||'),
			OperatorInfo(op_basic.ImplOperator, '->'),
			OperatorInfo(op_basic.XorOperator, '^'),
			OperatorInfo(op_basic.IffOperator, '<->'),
		),
	}

	default_prefix_ops = [
		OperatorInfo(op_basic.PositiveOperator, '+'),
		OperatorInfo(op_basic.NegativeOperator, '-'),
		OperatorInfo(op_basic.NotOperator, '~'),
		#OperatorInfo(op_utils.DecimalPointOperator, '.')
	]

	default_postfix_ops = [
		OperatorInfo(op_num.FactorialOperator, '!'),
	]

	return Parser(default_prefix_ops, default_postfix_ops, default_precedence_table)

def give_advanced_parser(additional_prefix = [], additional_postfix = []):
	default_precedence_table = {
		9: PrecedenceLayer.right_asso(
			*OperatorInfo.factory(op_num.PowOperator, '**', '^')
		),
		10: PrecedenceLayer.left_asso(
			OperatorInfo(op_basic.MultipleOperator, '*'),
			OperatorInfo(op_basic.DivideOperator, '/'),
			OperatorInfo(op_basic.IntegerDivideOperator, '//'),
			OperatorInfo(op_basic.ModuloOperator, '%'),
		),
		20: PrecedenceLayer.left_asso(
			OperatorInfo(op_basic.PlusOperator, '+'),
			OperatorInfo(op_basic.MinusOperator, '-'),
			OperatorInfo(op_basic.ConcatOperator, '.'),
		),
		70: PrecedenceLayer.left_asso(
			OperatorInfo(op_basic.LessOperator, '<'),
			OperatorInfo(op_basic.LeOperator, '<='),
			OperatorInfo(op_basic.GreaterOperator, '>'),
			OperatorInfo(op_basic.GeOperator, '>='),
		),
		80: PrecedenceLayer.left_asso(
			OperatorInfo(op_basic.EqualOperator, '=='),
			OperatorInfo(op_basic.NonequalOperator, '!='),
		),
		110: PrecedenceLayer.right_asso(
			*OperatorInfo.factory(op_basic.AndOperator, '&&', 'and'),
			*OperatorInfo.factory(op_basic.OrOperator, '||', 'or'),
			OperatorInfo(op_basic.ImplOperator, '->'),
			OperatorInfo(op_basic.XorOperator, 'xor'),
			OperatorInfo(op_basic.IffOperator, '<->'),
		),
		200: PrecedenceLayer.right_asso(
			OperatorInfo(op_assign.AssignOperator, '='),
			OperatorInfo(op_assign.DeclareOperator, ':='),
			OperatorInfo(op_assign.DeclareReferenceOperator, ':=&'),
		),
		10000: PrecedenceLayer.left_asso(
			OperatorInfo(op_utils.PassOperator, ';')
		),
	}

	default_prefix_ops = [
		OperatorInfo(op_basic.PositiveOperator, '+'),
		OperatorInfo(op_basic.NegativeOperator, '-'),
		*OperatorInfo.factory(op_basic.NotOperator, '~', 'not', '!'),
		OperatorInfo(op_num.AbsOperator, 'abs'),
		OperatorInfo(op_rng.RandomOperator, 'random'),
		OperatorInfo(op_rng.RandomWithSeedOperator, 'random'),
		OperatorInfo(op_str.LengthOperator, 'len'),
		OperatorInfo(op_str.StrictSymParseOperator, 'parse'),
		OperatorInfo(op_utils.PrintOperator, 'print'),
		OperatorInfo(op_utils.PassOperator, 'pass'),
		OperatorInfo(op_utils.DummizeOperator, 'dummy'),
		OperatorInfo(op_utils.DedummizeOperator, 'solid'),
		OperatorInfo(op_utils.ReverseOperator, 'reverse'),
		*OperatorInfo.factory(op_utils.RaiseOperator, 'raise', 'throw'),
		OperatorInfo(op_utils.DecimalPointOperator, '.'),
		OperatorInfo(op_utils.MoveOperator, 'move'),
	]

	default_postfix_ops = [
		OperatorInfo(op_num.FactorialOperator, '!'),
	]

	return Parser(default_prefix_ops + additional_prefix, default_postfix_ops + additional_postfix, default_precedence_table)
