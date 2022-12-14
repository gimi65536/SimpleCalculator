from .types import *
from .exceptions import UserDefinedError
from .ops import BinaryOperator, TernaryOperator, UnaryOperator
from .utils import filter_operator
from sympy.parsing.sympy_parser import auto_number, parse_expr, rationalize

class ToStringOperator(UnaryOperator):
	# Just do str() to the contents of the constants
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		return StringConstant(str(a.value))

class PrintOperator(UnaryOperator):
	# For numbers, the function returns expressions of primary types: int float complex
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if a.is_number:
			if a.is_('integer'):
				return StringConstant(str(a))
			if a.is_('real'):
				return StringConstant(str(a.value.evalf()))
			c = complex(a.simplify().value)
			real = str(int(c.real)) if c.real.is_integer() else str(c.real)
			imag = str(int(c.imag)) if c.imag.is_integer() else str(c.imag)
			return StringConstant(f'({real}+{imag}j)')
		else:
			return StringConstant(str(a.value))

class PassOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		return self.eval_operands(mapping, **kwargs)[1]

# It is weird to use reverse onto infix operators unless you know what you do
class ReverseOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		operand = self._operands[0]
		if isinstance(operand, Operator):
			node = type(operand)(*reversed(operand._operands))
			return node.eval(mapping, **kwargs)

		raise ValueError('Can only applied to an operation node')

class DummizeOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		return a.with_dummy()

class DedummizeOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		return a.without_dummy()

class RepeatTwiceOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		self.eval_operand(0, mapping, **kwargs)
		a = self.eval_operand(0, mapping, **kwargs)

		return a

class RepeatTimesOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)
		if a.is_number and a.is_('integer') and a.is_('positive'):
			n = a.simplify().value
			for _ in range(n):
				b = self.eval_operand(1, mapping, **kwargs)

			return b

		raise ValueError('Only accept positive integer as the first argument')

class RaiseOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		raise UserDefinedError(str(a))

class DecimalPointOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)
		if a.is_number and a.is_('integer') and a.is_('nonnegative'):
			n = a.simplify().value
			return NumberConstant(parse_expr(f'0.{n}', transformations = (auto_number, rationalize)))
		elif a.is_str and all(c.isdigit() for c in a.value):
			return NumberConstant(parse_expr(f'0.{a.value}', transformations = (auto_number, rationalize)))

		raise ValueError('Only apply to nonnegative integers or decimal strings')

class MoveOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		return self.eval_and_extract_constant(0, mapping, **kwargs)

class TypeOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)
		if a.is_number:
			return StringConstant('number')
		elif a.is_bool:
			return StringConstant('boolean')
		elif a.is_str:
			return StringConstant('string')

		raise ValueError('Unknown constant type')

__all__ = filter_operator(globals())
