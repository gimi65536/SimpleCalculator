from .types import *
from .ops import BinaryOperator, TernaryOperator, UnaryOperator
from .utils import *
from sympy import E, Expr, I, S
from sympy.parsing.sympy_parser import (
	parse_expr,
	repeated_decimals,
	auto_number,
	factorial_notation,
	convert_xor,
	implicit_multiplication,
	convert_equals_signs,
	rationalize
)

class LengthOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if not a.is_str:
			raise ValueError('Only apply to strings')

		return NumberConstant(S(len(a.value)))

'''
The function invokes a more flexible parser provided by SymPy with:
repeated_decimals (0.2[1] to 0.2111...), auto_number,
factorial_notation (5! = 120), convert_xor (3^2 is 3**2),
implicit_multiplication (sin(1)cos(1) is sin(1)*cos(1)),
convert_equals_signs (1 = 1 is 1 == 1), and rationalize
to parse a complicated numeric expressions into number constants.
This implies that the operator is independent from the parser
of the calculator, and users need to write expressions in terms of
what SymPy wants.

Specially, we make "i/j/J" be I, "e" be E, and 'Pi/PI' be pi.

Also, of course, the function using SymPy parser cannot handle any
assignment clauses to interfere the variable spaces.

Note that "=" is not equivalent to "==": "=" checks the symbolic
equivalence, e.g., "4*(5/2 - I)*(10 + 4*I)/29 = 4",
but "==" checks whether two expressions are "exactly" same,
e.g., "4*(5/2 - I)*(10 + 4*I)/29 != 4"
("2+2 == 4" is True because "2+2" will be *implicitly*
evaluated to "4").

Therefore, an equality check with variables "x = 5" CANNOT be written
in "x == 5" because "'x' is a variable, not exactly a constant 5."
We solve this problem by inputing all the information of the contexts
(mapping) to local_dict.
However, this solution hurts performance when the contexts are extremely large.
Worse, it still cannot solve the problem in "x == n" if either "x" or "n" denotes
complicated expressions such as "4*(5/2 - I)*(10 + 4*I)/29"
but the other denotes "4".

USE "=" INSTEAD OF "==" IF POSSUBLE TO GET WHAT YOU WANT, ANYWAY.
'''
class SymParseOperator(UnaryOperator):
	def eval(self, mapping, **kwargs):
		a = self.eval_and_extract_constant(0, mapping, **kwargs)

		if not a.is_str:
			raise ValueError('Only apply to strings')

		s = a.value

		# Boolean parse
		if s == 'TRUE' or s == 'True' or s == 'true':
			return BooleanConstant(True)
		elif s == 'FALSE' or s == 'False' or s == 'false':
			return BooleanConstant(False)

		mapping = mapping_flatten(mapping)
		local_dict = {
			'i': I,
			'j': I,
			'J': I,
			'e': E,
			'Pi': S.Pi,
			'PI': S.Pi,
		}
		local_dict.update({v.name: lv.content for v, lv in mapping.items()})

		try:
			n = parse_expr(s, transformations = (
				repeated_decimals,
				auto_number,
				factorial_notation,
				convert_xor,
				implicit_multiplication,
				convert_equals_signs,
				rationalize
			), local_dict = local_dict)

			if isinstance(n, bool):
				return BooleanConstant(n)

			n = n.simplify()

			if isinstance(n, Expr):
				return NumberConstant(n)
			elif n is S.true:
				return BooleanConstant(True)
			elif n is S.false:
				return BooleanConstant(False)
		except:
			pass

		return a.without_dummy()

class StrictSymParseOperator(SymParseOperator):
	def eval(self, mapping, **kwargs):
		result = super().eval(mapping, **kwargs)

		if result.is_str:
			raise ValueError(f'Cannot parse {result.value} into a number/Boolean value')

		return result
