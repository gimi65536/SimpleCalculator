from .types import *
from .ops import BinaryOperator, TernaryOperator, UnaryOperator
import sympy

class AbsOperator(UnaryOperator):
	def eval(self, mapping):
		a = self.extract_constant(*self.eval_operands(mapping))[0]

		if not a.is_number:
			raise ValueError('Only apply to numbers')

		return NumberConstant(sympy.Abs(a.value))

class PowOperator(BinaryOperator):
	def eval(self, mapping):
		a, b = self.extract_constant(*self.eval_operands(mapping))

		if a.is_number and b.is_number:
			return NumberConstant(a.value ** b.value)

		raise ValueError('Only apply to numbers')

class FactorialOperator(UnaryOperator):
	def eval(self, mapping):
		a = self.extract_constant(*self.eval_operands(mapping))[0]

		if not a.is_number:
			raise ValueError('Only apply to numbers')

		n = a.value
		if n.is_integer and n.is_nonnegative:
			return NumberConstant(sympy.factorial(n))
		else:
			raise ValueError('Only accepts nonnegative integer')

class RealOperator(UnaryOperator):
	def eval(self, mapping):
		a = self.extract_constant(*self.eval_operands(mapping))[0]

		if not a.is_number:
			raise ValueError('Only apply to numbers')

		return NumberConstant(sympy.re(a.value))

class ImagOperator(UnaryOperator):
	def eval(self, mapping):
		a = self.extract_constant(*self.eval_operands(mapping))[0]

		if not a.is_number:
			raise ValueError('Only apply to numbers')

		return NumberConstant(sympy.im(a.value))
