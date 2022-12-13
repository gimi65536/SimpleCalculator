from .types import *
from .ops import BinaryOperator
from sympy import Integer

TEMPVAR = object()

class AssignOperator(BinaryOperator):
	def eval(self, mapping):
		a, b = self.eval_operands(mapping)
		b = self.extract_constant(b)

		if not a.is_lvalue:
			raise ValueError('Only applies for variables')

		a.content = b.without_dummy()
		return a

class AssignWithAnonymousOperator(BinaryOperator):
	def eval(self, mapping):
		a = self._operands[0]
		if isinstance(a, Var) and a not in mapping:
			var = Var(a.name, TEMPVAR)
			lv = LValue(var, NumberConstant(Integer(0)))
			mapping[var] = lv

		a, b = self.eval_operands(mapping)
		b = self.extract_constant(b)

		if not a.is_lvalue:
			raise ValueError('Only applies for variables')

		a.content = b.without_dummy()
		return a
