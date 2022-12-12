from __future__ import annotations
from collections.abc import Callable, Mapping
from sympy import Expr, floor, Integer, simplify
from sympy.codegen.cfunctions import log10
from typing import Any, Generic, TypeVar, Union

class TreeNodeType:
	def eval(self, mapping: Mapping[Var, LValue]) -> Value:
		raise NotImplementedError

	def apply_var(self, f: Callable[[Var], Any]):
		raise NotImplementedError

class Value:
	_is_constant: bool = False
	_is_lvalue: bool = False

	@property
	def is_constant(self):
		return self._is_constant

	@property
	def is_lvalue(self):
		return self._is_lvalue

class Var(TreeNodeType):
	_name: str
	_scope: Any # None for "weird" or "naive" variables

	def __init__(self, name, scope = None):
		self._name = name
		self._scope = scope

	def __repr__(self):
		if self._scope is None:
			return self._name
		else:
			return f'<{self._scope}.{self._name}>'

	@property
	def name(self) -> str:
		return self._name

	@property
	def scope(self) -> Any:
		return self._scope

	@scope.setter
	def scope(self, s: Any):
		self._scope = s

	def eval(self, mapping):
		if self not in mapping:
			raise ValueError(f'Variable "{self._name}" is undefined')

		return mapping[self]

	def apply_var(self, f):
		f(self)

	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return NotImplemented

		if self._name != other._name:
			return False

		if self._scope is None or other._scope is None:
			return True

		return self._scope == other._scope

	def __hash__(self):
		return hash(self._name)

ConstType = TypeVar('ConstType', Expr, bool, str)

class Constant(TreeNodeType, Value, Generic[ConstType]):
	_is_number: bool
	_is_bool: bool
	_is_str: bool

	_is_dummy: bool = False

	_is_constant = True

	@classmethod
	def create_dummy(cls, dummy_value: ConstType):
		result = cls(dummy_value)
		result._is_dummy = True
		return result

	def with_dummy(self):
		if self.is_dummy:
			return self

		return type(self).create_dummy(self._value)

	def without_dummy(self):
		if not self.is_dummy:
			return self

		return type(self)(self._value)

	def __init__(self, value: ConstType):
		self._value = value

	def __str__(self):
		return str(self._value)

	def __repr__(self):
		return repr(self._value)

	@property
	def value(self) -> ConstType:
		return self._value

	def eval(self, mapping):
		return self

	def apply_var(self, f):
		pass

	def __eq__(self, other):
		# Only True if the type is same
		if type(self) is not type(other):
			return NotImplemented

		return self._value == other._value

	def cast(self, to_type: type[Constant]):
		raise NotImplementedError

	def to_number(self) -> NumberConstant:
		return self.cast(NumberConstant)

	def to_bool(self) -> BooleanConstant:
		return self.cast(BooleanConstant)

	def to_str(self) -> StringConstant:
		return self.cast(StringConstant)

	@property
	def is_number(self) -> bool:
		return self._is_number

	@property
	def is_bool(self) -> bool:
		return self._is_bool

	@property
	def is_str(self) -> bool:
		return self._is_str

	'''
	Dummy notates whether a constant is "processed" in the semantics even
	if the function returns input constant object directly in the
	implementation.
	For example, the prefix operator "+" does nothing and returns the input
	number constant, but it is "processed" in the semantics, so it needs to
	de-dummy the constant before returning.
	By contrast, the pass operator (the comma operator in C/C++), the value
	at right should be returned instantly without any additional processing,
	so the dummy attribute will remain.
	'''
	@property
	def is_dummy(self) -> bool:
		return self._is_dummy

class NumberConstant(Constant[Expr]):
	_is_number = True
	_is_bool = False
	_is_str = False
	# This shared dict is warranted to be thread-safe because for every expr, there is only
	# one possible simplified expr.
	_simplify_cache: dict[Expr, Expr] = {}
	# The term "Number" in our program includes all complex numbers
	# So it is possible to have many "types" of SymPy data other than "SymPy.Number" 
	# such as I (ImaginaryUnit), 3*I (Mul), or 1+3*I (Add), they are not instances of SymPy.Number

	# In general that will cause problems if we don't restrict the Expr types used
	# Thus the value expressions should satisfy "is_number"
	def __init__(self, value):
		assert value.is_number
		super().__init__(value)

	def __str__(self):
		return str(self._simplify())

	def _simplify(self) -> Expr:
		if self._value not in self._simplify_cache:
			self._simplify_cache[self._value] = self._value.simplify()
		return self._simplify_cache[self._value]

	def simplify(self) -> NumberConstant:
		return NumberConstant(self._simplify())

	def is_(self, what):
		result = getattr(self._value, f'is_{what}')
		if result is None:
			result = getattr(self._simplify(), f'is_{what}')
		return result

	def cast(self, to_type):
		if to_type is NumberConstant:
			return self
		elif to_type is BooleanConstant:
			return BooleanConstant(bool(self._simplify()))
		elif to_type is StringConstant:
			s, v = '', self._simplify()
			if v.is_integer:
				s = str(int(v))
			elif v.is_Rational:
				# Rational but not integer
				p, q = v.p, v.q
				factors = Integer(q).factors()
				p2 = factors.pop(2, 0)
				p5 = factors.pop(5, 0)
				if len(factors) > 0:
					# Infinite (Regular) decimal
					s = str(v.evalf())
				else:
					if p2 > p5:
						q *= 5 ** (p2 - p5)
						p *= 5 ** (p2 - p5)
					elif p5 > p2:
						q *= 2 ** (p5 - p2)
						p *= 2 ** (p5 - p2)

					precision = log10(q)
					assert precision.is_Integer
					digit_of_p = floor(log10(p)) + 1
					if precision < digit_of_p:
						# x--x.y--y [y--y: precision]
						s = str(p)
						s = s[:(digit_of_p - precision)] + "." + s[(digit_of_p - precision):]
					else:
						s = "0." + ("0" * (precision - digit_of_p)) + str(p)
			elif v.is_Float:
				s = str(v.evalf())
			elif v.is_irrational:
				# Other real numbers
				s = str(v.evalf())
			else:
				s = str(complex(v))

			return StringConstant(s)

class BooleanConstant(Constant[bool]):
	_is_number = False
	_is_bool = True
	_is_str = False

	def cast(self, to_type):
		if to_type is NumberConstant:
			return NumberConstant(simplify(int(self._value)))
		elif to_type is BooleanConstant:
			return self
		elif to_type is StringConstant:
			return StringConstant(str(self._value))

class StringConstant(Constant[str]):
	_is_number = False
	_is_bool = False
	_is_str = True

	def cast(self, to_type):
		if to_type is NumberConstant:
			return NumberConstant(simplify(self._value))
		elif to_type is BooleanConstant:
			return BooleanConstant(bool(self._value))
		elif to_type is StringConstant:
			return self

class LValue(Value):
	_is_lvalue = True

	def __init__(self, var: Var, const: Constant, bookkeeping: dict[LValue, tuple[Constant, Constant]] = {}):
		self._var = var
		self._content = const
		self._bookkeeping = bookkeeping

	def __repr__(self):
		return f'<{self._var}: {self._content}>'

	@property
	def var(self):
		return self._var

	@property
	def content(self) -> Constant:
		return self._content

	@content.setter
	def content(self, const: Constant):
		if self in self._bookkeeping:
			self._content = const
			ori = self._bookkeeping[self][0]
			if ori == const:
				self._bookkeeping.pop(self)
			else:
				self._bookkeeping[self] = (ori, const)
		else:
			ori = self._content
			if ori != const:
				self._content = const
				self._bookkeeping[self] = (ori, const)

	@property
	def value(self):
		return self._content.value

class Operator(TreeNodeType):
	# An immutable type
	ary: int
	_operands: list[TreeNodeType]

	def __init__(self, *args: TreeNodeType):
		if len(args) != self.ary:
			raise ValueError('Unmatched numbers of operands.')

		self._operands = args

	def __repr__(self):
		return type(self).__name__ + '(' + ', '.join(repr(o) for o in self._operands) + ')'

	def eval(self, mapping):
		raise NotImplementedError

	def eval_operand(self, i: int, mapping: Mapping[Var, LValue]) -> Value:
		return self._operands[i].eval(mapping)

	def eval_operands(self, mapping: Mapping[Var, LValue]) -> list[Value]:
		return [o.eval(mapping) for o in self._operands]

	def eval_and_extract_constant(self, i: int, mapping: Mapping[Var, LValue]) -> Constant:
		return self.extract_constant(self.eval_operand(i, mapping))

	def eval_and_extract_constants(self, mapping: Mapping[Var, LValue]) -> list[Constant]:
		return self.extract_constants(*self.eval_operands(mapping))

	def apply_var(self, f):
		for o in self._operands:
			o.apply_var(f)

	@staticmethod
	def extract_constant(value: Value) -> Constant:
		if isinstance(value, Constant):
			return value
		else:
			return value.content

	@classmethod
	def extract_constants(cls, *args: Value) -> list[Constant]:
		return [cls.extract_constant(v) for v in args]
