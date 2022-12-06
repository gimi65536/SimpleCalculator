from .types import *
from .ops import BinaryOperator, TernaryOperator, UnaryOperator
from sympy import E, Expr, I, S
from sympy.parsing.sympy_parser import (
	parse_expr,
	auto_symbol,
	repeated_decimals,
	auto_number,
	factorial_notation,
	convert_xor,
	implicit_multiplication,
	convert_equals_signs,
	rationalize
)

class LengthOperator(UnaryOperator):
	def eval(self, mapping):
		a = self.extract_constant(*self.eval_operands(mapping))[0]

		if not a.is_str:
			raise ValueError('Only apply to strings')

		return NumberConstant(len(a.value))

'''
The function invokes a more flexible parser provided by SymPy with:
auto_symbol, repeated_decimals (0.2[1] to 0.2111...), auto_number,
factorial_notation (5! = 120), convert_xor (3^2 is 3**2),
implicit_multiplication (sin(1)cos(1) is sin(1)*cos(1)),
convert_equals_signs (1 = 1 is 1 == 1), and rationalize
to parse a complicated numeric expressions into number constants.
This implies that the operator is independent from the parser
of the calculator, and users need to write expressions in terms of
what SymPy wants.

Specially, we make "i/j/J" be I, "e" be E, and 'Pi/PI' be pi.

Note that an equality check with variables "x = 5" CANNOT be written
in "x == 5" because "'x' is a variable, not a constant 5."

Also, of course, the function using SymPy parser cannot handle any
assignment clauses to interfere the variable spaces.
'''
class SymParseOperator(UnaryOperator):
	def eval(self, mapping):
		a = self.extract_constant(*self.eval_operands(mapping))[0]

		if not a.is_str:
			raise ValueError('Only apply to strings')

		s = a.value

		# Boolean parse
		if s == 'TRUE' or s == 'True' or s == 'true':
			return BooleanConstant(True)
		elif s == 'FALSE' or s == 'False' or s == 'false':
			return BooleanConstant(False)

		try:
			expr = parse_expr(s, transformations = (
				auto_symbol,
				repeated_decimals,
				auto_number,
				factorial_notation,
				convert_xor,
				implicit_multiplication,
				convert_equals_signs,
				rationalize
			), local_dict = {
				'i': I,
				'j': I,
				'J': I,
				'e': E,
				'Pi': S.Pi,
				'PI': S.Pi,
			})
			free_symbols = expr.free_symbols
			subs = {}
			for symbol in free_symbols:
				v = Var(symbol)
				if v not in mapping:
					raise ValueError(f'The expression includes undefined variable {symbol}')
				c = mapping.get(v).content
				if c.is_str:
					raise ValueError(f'The variable {symbol} is a string')
				if c.is_bool:
					if c.value:
						subs[symbol] = S.true
					else:
						subs[symbol] = S.false
				else:
					subs[symbol] = c.value

			n = expr.subs(subs)

			if isinstance(n, Expr):
				return NumberConstant(n)
			elif n is S.true:
				return BooleanConstant(True)
			elif n is S.false:
				return BooleanConstant(False)
		except:
			pass

		return a

class StrictSymParseOperator(ParseOperator):
	def eval(self, mapping):
		result = super().eval(mapping)

		if result.is_str:
			raise ValueError(f'Cannot parse {result.value} into a number/Boolean value')

		return result