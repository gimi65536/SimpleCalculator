from .types import *
from collections.abc import Mapping

# Simply pick the firstly encountered variable.
def mapping_flatten(mapping: Mapping[Var, LValue]) -> Mapping[Var, LValue]:
	d = {}
	for v, lv in mapping.items():
		var = Var(v.name)
		if var in d:
			continue

		d[var] = lv

	return d

def filter_operator(g: dict[str, object]) -> list[str]:
	return [name for name in g if
		not name.startswith('_') and
		name.endswith('Operator') and
		name not in ('Operator', 'NullaryOperator', 'UnaryOperator', 'BinaryOperator', 'TernaryOperator')
	]

__all__ = (
	'mapping_flatten',
	'filter_operator',
)
