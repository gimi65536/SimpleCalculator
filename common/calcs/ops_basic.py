from .types import *
from .ops import BinaryOperator, TernaryOperator, UnaryOperator

class PlusOperator(BinaryOperator):
	def eval(self):
		a, b = self.extract_constant(*self.eval_operands())

		if a.is_str or b.is_str:
			a, b = a.to_str(), b.to_str()
			return StringConstant(a.value + b.value)
		elif a.is_bool and b.is_bool:
			return BooleanConstant(a.value or b.value)
		else:
			a, b = a.to_number(), b.to_number()
			return NumberConstant(a.value + b.value)

class MinusOperator(BinaryOperator):
	def eval(self):
		a, b = self.extract_constant(*self.eval_operands())

		if a.is_str or b.is_str:
			raise ValueError('Invalid string subtraction')
		elif a.is_bool and b.is_bool:
			return BooleanConstant(a.value and not b.value)
		else:
			a, b = a.to_number(), b.to_number()
			return NumberConstant(a.value - b.value)

class MultipleOperator(BinaryOperator):
	def eval(self):
		a, b = self.extract_constant(*self.eval_operands())

		if a.is_str or b.is_str:
			# a:num/bool b:str
			if a.is_str:
				a, b = b, a

			if a.is_str:
				# Both a, b are str
				raise ValueError('Invalid string multiplication')

			if a.is_bool:
				a = a.to_number()

			if not (a.value.is_integer and a.value.nonnegative):
				raise ValueError('String multiplication is valid only for non-negative integer')

			return StringConstant(a.value * b.value)
		elif a.is_bool and b.is_bool:
			return BooleanConstant(a.value and b.value)
		else:
			a, b = a.to_number(), b.to_number()
			return NumberConstant(a.value * b.value)

class DivideOperator(BinaryOperator):
	def eval(self):
		a, b = self.extract_constant(*self.eval_operands())

		if a.is_number and b.is_number:
			return NumberConstant(a.value / b.value)
		else:
			raise ValueError('Invalid type division')

class IntegerDivideOperator(BinaryOperator):
	def eval(self):
		a, b = self.extract_constant(*self.eval_operands())

		if a.is_number and b.is_number:
			return NumberConstant(a.value // b.value)
		else:
			raise ValueError('Invalid type division')

class ModuloOperator(BinaryOperator):
	def eval(self):
		a, b = self.extract_constant(*self.eval_operands())

		if a.is_number and b.is_number:
			return NumberConstant(a.value % b.value)
		else:
			raise ValueError('Invalid type division')

class PositiveOperator(UnaryOperator):
	def eval(self):
		a = self.extract_constant(*self.eval_operands())[0]

		if a.is_number:
			return a
		else:
			raise ValueError('Only positive number')

class NegativeOperator(UnaryOperator):
	def eval(self):
		a = self.extract_constant(*self.eval_operands())[0]

		if a.is_number:
			return NumberConstant(-a.value)
		else:
			raise ValueError('Only negative number')

class NotOperator(UnaryOperator):
	def eval(self):
		a = self.extract_constant(*self.eval_operands())[0]

		if a.is_bool:
			return BooleanConstant(not a.value)
		else:
			a = a.to_bool()
			return BooleanConstant(not a.value)

class _BinaryBoolOperator(BinaryOperator):
	def eval(self):
		a, b = self.extract_constant(*self.eval_operands())

		a, b = a.to_bool(), b.to_bool()
		return BooleanConstant(self._logic(a.value, b.value))

	def _logic(self, a: bool, b: bool, /):
		raise NotImplementedError

class AndOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return a and b

class OrOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return a or b

class ImplOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return not a or b

class NimplOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return a and not b

class XorOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return a != b

class IffOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return a == b

class NandOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return not(a and b)

class NorOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return not(a or b)

# The below two operators are rarely used and I will not use them
# Of course these two ops are here to invoke for free

class ConverseImplOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return a or not b

class ConverseNimplOperator(_BinaryBoolOperator):
	def _logic(self, a, b, /):
		return not a and b

class ConcatOperator(BinaryOperator):
	def eval(self):
		a, b = self.extract_constant(*self.eval_operands())

		a, b = a.to_str(), b.to_str()
		return StringConstant(a.value + b.value)

class IfThenElseOperator(TernaryOperator):
	def eval(self):
		a, b, c = self.eval_operands()
		a = a.extract_constant(a)[0]
		a = a.to_bool()

		if a.value:
			return b
		else:
			return c
