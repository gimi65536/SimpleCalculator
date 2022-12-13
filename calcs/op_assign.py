from .types import *
from .ops import BinaryOperator
from .utils import filter_operator

class AssignOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_operands(mapping, **kwargs)
		b = self.extract_constant(b)

		if not a.is_lvalue:
			raise ValueError('Only applies for variables')

		a.content = b.without_dummy()
		return a

class DeclareOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a = self._operands[0]
		if isinstance(a, Var):
			b = self.eval_and_extract_constant(1, mapping, **kwargs)

			if a in mapping:
				raise ValueError(f'The variable {a.name} has existed')

			# Not a temporary anonymous var
			# It has a naive scope and no bookkeeping
			var = Var(a.name, None)
			lv = LValue(var, b.without_dummy())
			mapping[var] = lv
			return lv

		raise ValueError('A variable name is needed')

class DeclareReferenceOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a = self._operands[0]
		if isinstance(a, Var):
			b = self.eval_operand(1, mapping, **kwargs)

			if a in mapping:
				raise ValueError(f'The variable {a.name} has existed')
			if not b.is_lvalue:
				raise ValueError(f'Expect an l-value')

			# Not a temporary anonymous var
			# It has a naive scope and no bookkeeping
			var = Var(a.name, None)
			mapping[var] = b
			return b

		raise ValueError('A variable name is needed')

__all__ = filter_operator(globals())
