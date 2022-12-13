from .types import *
from .ops import BinaryOperator, TernaryOperator, UnaryOperator
from .utils import filter_operator
from sympy import Eq, Expr, Ne
from typing import Optional, overload

class PlusOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if a.is_str or b.is_str:
			a, b = a.to_str(), b.to_str()
			return StringConstant(a.value + b.value)
		elif a.is_bool and b.is_bool:
			return BooleanConstant(a.value or b.value)
		else:
			a, b = a.to_number(), b.to_number()
			return NumberConstant(a.value + b.value)

class MinusOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if a.is_str or b.is_str:
			raise ValueError('Invalid string subtraction')
		elif a.is_bool and b.is_bool:
			return BooleanConstant(a.value and not b.value)
		else:
			a, b = a.to_number(), b.to_number()
			return NumberConstant(a.value - b.value)

class MultipleOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if a.is_str or b.is_str:
			# a:num/bool b:str
			if a.is_str:
				a, b = b, a

			if a.is_str:
				# Both a, b are str
				raise ValueError('Invalid string multiplication')

			if a.is_bool:
				a = a.to_number()

			n = a.simplify().value
			if not (n.is_integer and n.is_nonnegative):
				raise ValueError('String multiplication is valid only for non-negative integer')

			return StringConstant(n * b.value)
		elif a.is_bool and b.is_bool:
			return BooleanConstant(a.value and b.value)
		else:
			a, b = a.to_number(), b.to_number()
			return NumberConstant(a.value * b.value)

class DivideOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if a.is_number and b.is_number:
			return NumberConstant(a.value / b.value)
		else:
			raise ValueError('Invalid type division')

class IntegerDivideOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if a.is_number and b.is_number:
			return NumberConstant(a.value // b.value)
		else:
			raise ValueError('Invalid type division')

class ModuloOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if a.is_number and b.is_number:
			return NumberConstant(a.value % b.value)
		else:
			raise ValueError('Invalid type division')

class PositiveOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if a.is_number:
			return a.without_dummy()
		else:
			raise ValueError('Only positive number')

class NegativeOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if a.is_number:
			return NumberConstant(-a.value)
		else:
			raise ValueError('Only negative number')

class NotOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if a.is_bool:
			return BooleanConstant(not a.value)
		else:
			a = a.to_bool()
			return BooleanConstant(not a.value)

class _BinaryBoolOperator(BinaryOperator):
	_shortcut: bool = True

	def eval(self, mapping, **kwargs):
		if self._shortcut:
			a = self.eval_and_extract_constant(0, mapping, **kwargs).to_bool()
			result = self._logic(a.value)

			if result is not None:
				return BooleanConstant(result)

			b = self.eval_and_extract_constant(1, mapping, **kwargs).to_bool()
			return BooleanConstant(self._logic(a.value, b.value))
		else:
			a, b = self.eval_and_extract_constants(mapping, **kwargs)

			a, b = a.to_bool(), b.to_bool()
			return BooleanConstant(self._logic(a.value, b.value))

	@overload
	def _logic(self, a: bool, /) -> Optional[bool]:
		...

	@overload
	def _logic(self, a: bool, b: bool, /) -> bool:
		...

	def _logic(self, a, b = None, /):
		raise NotImplementedError

	@staticmethod
	def _not(b: Optional[bool]):
		return None if b is None else (not b)

class AndOperator(_BinaryBoolOperator):
	def _logic(self, a, b = None, /):
		if a:
			return b
		else:
			return False

class OrOperator(_BinaryBoolOperator):
	def _logic(self, a, b = None, /):
		if not a:
			return b
		else:
			return True

class ImplOperator(_BinaryBoolOperator):
	def _logic(self, a, b = None, /):
		if a:
			return b
		else:
			return True

class NimplOperator(_BinaryBoolOperator):
	def _logic(self, a, b = None, /):
		if a:
			return self._not(b)
		else:
			return False

class XorOperator(_BinaryBoolOperator):
	_shortcut = False
	def _logic(self, a, b = None, /):
		return a != b

class IffOperator(_BinaryBoolOperator):
	_shortcut = False
	def _logic(self, a, b = None, /):
		return a == b

class NandOperator(_BinaryBoolOperator):
	def _logic(self, a, b = None, /):
		if a:
			return self._not(b)
		else:
			return True

class NorOperator(_BinaryBoolOperator):
	def _logic(self, a, b = None, /):
		if not a:
			return self._not(b)
		else:
			return False

# The below two operators are rarely used and I will not use them
# Of course these two ops are here to invoke for free

class ConverseImplOperator(_BinaryBoolOperator):
	def _logic(self, a, b = None, /):
		if not a:
			return self._not(b)
		else:
			return True

class ConverseNimplOperator(_BinaryBoolOperator):
	def _logic(self, a, b = None, /):
		if not a:
			return b
		else:
			return False

class ConcatOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		a, b = a.to_str(), b.to_str()
		return StringConstant(a.value + b.value)

class IfThenElseOperator(TernaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_operand(0, mapping, **kwargs)
		a = a.extract_constant(a)[0]
		a = a.to_bool()

		if a.value:
			return self.eval_operand(1, mapping, **kwargs)
		else:
			return self.eval_operand(2, mapping, **kwargs)

class EqualOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if type(a) != type(b):
			return BooleanConstant(False)

		return BooleanConstant(bool(Eq(a.value, b.value).simplify()))

class NonequalOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		if type(a) != type(b):
			return BooleanConstant(True)

		return BooleanConstant(bool(Ne(a.value, b.value).simplify()))

class _BinaryComparisonOperator(BinaryOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)
		if a.is_bool:
			a = a.to_number()
		if b.is_bool:
			b = b.to_number()

		if a.is_number and b.is_number:
			if a.is_('real') and b.is_('real'):
				return BooleanConstant(self._comp(a.value, b.value))
			else:
				return BooleanConstant(bool(Eq(a.value, b.value).simplify()))
		elif a.is_str and b.is_str:
			return BooleanConstant(self._compstr(a.value, b.value))
		else:
			raise ValueError('Unable to compare between string and number/Boolean')

	def _comp(self, a: Expr, b: Expr, /) -> bool:
		# @Pre is_real
		raise NotImplementedError

	def _compstr(self, a: str, b: str, /) -> bool:
		raise NotImplementedError

class LessOperator(_BinaryComparisonOperator):
	def _comp(self, a, b, /):
		return bool((a < b).simplify())

	def _compstr(self, a, b, /):
		return a < b

class LeOperator(_BinaryComparisonOperator):
	def _comp(self, a, b, /):
		return bool((a <= b).simplify())

	def _compstr(self, a, b, /):
		return a <= b

class GreaterOperator(_BinaryComparisonOperator):
	def _comp(self, a, b, /):
		return bool((a > b).simplify())

	def _compstr(self, a, b, /):
		return a > b

class GeOperator(_BinaryComparisonOperator):
	def _comp(self, a, b, /):
		return bool((a >= b).simplify())

	def _compstr(self, a, b, /):
		return a >= b

__all__ = filter_operator(globals())
