from .types import *
from .ops import BinaryOperator, TernaryOperator, UnaryOperator
import sympy

class AbsOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if not a.is_number:
			raise ValueError('Only apply to numbers')

		return NumberConstant(sympy.Abs(a.value))

class PowOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if a.is_number and b.is_number:
			return NumberConstant(a.value ** b.value)

		raise ValueError('Only apply to numbers')

class FactorialOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if not a.is_number:
			raise ValueError('Only apply to numbers')

		if a.is_('integer') and a.is_('nonnegative'):
			return NumberConstant(sympy.factorial(a.value))
		else:
			raise ValueError('Only accepts nonnegative integer')

class RealOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if not a.is_number:
			raise ValueError('Only apply to numbers')

		return NumberConstant(sympy.re(a.value))

class ImagOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if not a.is_number:
			raise ValueError('Only apply to numbers')

		return NumberConstant(sympy.im(a.value))

# ++x
class IncrementOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_operand(0, mapping, **kwargs)
		if a.is_lvalue and a.content.is_number:
			a.content = NumberConstant(a.content.value + 1)
			return a

		raise ValueError('Only apply to number variables')

# x++
class PostIncrementOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_operand(0, mapping, **kwargs)
		if a.is_lvalue and a.content.is_number:
			result = a.content
			a.content = NumberConstant(result.value + 1)
			return result.without_dummy()

		raise ValueError('Only apply to number variables')

# --x
class DecrementOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_operand(0, mapping, **kwargs)
		if a.is_lvalue and a.content.is_number:
			a.content = NumberConstant(a.content.value - 1)
			return a

		raise ValueError('Only apply to number variables')

# x--
class PostDecrementOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_operand(0, mapping, **kwargs)
		if a.is_lvalue and a.content.is_number:
			result = a.content
			a.content = NumberConstant(result.value - 1)
			return result.without_dummy()

		raise ValueError('Only apply to number variables')
