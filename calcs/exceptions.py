class UserDefinedError(Exception):
	def __init__(self, msg):
		self.msg = msg

class LexerConstructError(ValueError):
	pass

class TokenizeError(ValueError):
	def __init__(self, position: int, s: str):
		super().__init__(position, s)

	def __str__(self):
		return f'At column {self.args[0]}: {self.args[1]}'

class ParserConstructError(ValueError):
	pass

class ParseError(ValueError):
	def __init__(self, position: int, s: str):
		super().__init__(position, s)

	def __str__(self):
		return f'At column {self.args[0]}: {self.args[1]}'
