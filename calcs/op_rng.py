from .types import *
from .ops import BinaryOperator, NullaryOperator, TernaryOperator, UnaryOperator
from sympy import ceiling, Float, floor, Integer, Number
from sympy.core.random import rng, random_complex_number

class RandomOperator(NullaryOperator):
	def eval(self, mapping, **kwargs):
		return NumberConstant(Float(rng.random()))

class RandomWithSeedOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if not a.is_dummy:
			rng.seed(str(a))

		return NumberConstant(Float(rng.random()))

class SetSeedOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)
		rng.seed(str(a))
		return BooleanConstant(True)

class _RandomRangeOperator:
	def _eval(self, a: Constant, b: Constant, c: Constant, seed = None):
		if a.is_number and b.is_number and c.is_number:
			na, nb, nc = a.value, b.value, c.value
			steps = ((nb - na) / nc).simplify()
			if not steps.is_real or steps < 0:
				raise ValueError('Invalid range')

			if seed is not None and not seed.is_dummy:
				rng.seed(str(seed))

			return NumberConstant(na + nc * rng.randint(0, floor(steps)))

		raise ValueError('Only apply numbers as input')

class RandomRangeZeroOperator(UnaryOperator, _RandomRangeOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		return self._eval(NumberConstant(Integer(0)), a, NumberConstant(Integer(1)))

class RandomRangeZeroWithSeedOperator(BinaryOperator, _RandomRangeOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(NumberConstant(Integer(0)), a, NumberConstant(Integer(1)), b)

class RandomRangeStepOneOperator(BinaryOperator, _RandomRangeOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b, NumberConstant(Integer(1)))

class RandomRangeStepOneWithSeedOperator(TernaryOperator, _RandomRangeOperator):
	def eval(self, mapping, **kwargs):
		a, b, c = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b, NumberConstant(Integer(1)), c)

class RandomRangeOperator(TernaryOperator, _RandomRangeOperator):
	def eval(self, mapping, **kwargs):
		a, b, c = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b, c)

class RandomRangeWithSeedOperator(Operator, _RandomRangeOperator):
	ary = 4
	def eval(self, mapping, **kwargs):
		a, b, c, d = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b, c, d)

class _RandomIntOperator:
	def _eval(self, a: Constant, b: Constant, seed = None):
		if (a.is_number and b.is_number) and (a.value.is_real and b.value.is_real):
			if a.value > b.value:
				a, b = b, a
			na = ceiling(a.value)
			nb = floor(b.value)
			if na > nb:
				raise ValueError('Not valid interval: no integer is included')

			if seed is not None and not seed.is_dummy:
				rng.seed(str(seed))

			return NumberConstant(Integer(rng.randint(int(na), int(nb))))

		raise ValueError('Only apply real numbers as input')

class RandomIntOperator(BinaryOperator, _RandomIntOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b)

class RandomIntWithSeedOperator(TernaryOperator, _RandomIntOperator):
	def eval(self, mapping, **kwargs):
		s, a, b = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b, s)

class _RandomRealOperator:
	def _eval(self, a: Constant, b: Constant, seed = None):
		if (a.is_number and b.is_number) and (a.value.is_real and b.value.is_real):
			if seed is not None and not seed.is_dummy:
				rng.seed(str(seed))

			return NumberConstant(Number(rng.uniform(a.value, b.value)))

		raise ValueError('Only apply real numbers as input')

class RandomRealOperator(BinaryOperator, _RandomRealOperator):
	def eval(self, mapping, **kwargs):
		a, b = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b)

class RandomRealWithSeedOperator(TernaryOperator, _RandomRealOperator):
	def eval(self, mapping, **kwargs):
		s, a, b = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b, s)

class _RandomComplexOperator:
	def _eval(self, a: Constant, b: Constant, c: Constant, d: Constant, seed = None):
		if (a.is_number and b.is_number) and (a.value.is_real and b.value.is_real and c.value.is_real and d.value.is_real):
			if seed is not None and not seed.is_dummy:
				rng.seed(str(seed))

			return NumberConstant(random_complex_number(a.value, c.value, b.value, d.value))

		raise ValueError('Only apply real numbers as input')

class RandomComplexOperator(Operator, _RandomComplexOperator):
	ary = 4
	def eval(self, mapping, **kwargs):
		a, b, c, d = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b, c, d)

class RandomComplexWithSeedOperator(Operator, _RandomComplexOperator):
	ary = 5
	def eval(self, mapping, **kwargs):
		s, a, b, c, d = self.eval_and_extract_constants(mapping, **kwargs)

		return self._eval(a, b, c, d, s)
