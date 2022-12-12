from distutils.core import setup

setup(
	name = 'SimpleCalculator',
	version = '0.0.2',
	description = 'Simple calculator',
	packages = ['calcs'],
	install_requires = [
		'more_itertools>=9',
		'sympy>=1.11.1'
	]
)
