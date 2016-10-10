class Scope(object):

	def __init__(self, parent = None):
		self.store = {}
		self.parent = parent

	def __getitem__(self, key):
		try:
			return self.store[key]
		except KeyError:
			try:
				return self.parent[key]
			except KeyError:
				raise NotImplementedError

	def __setitem__(self, key, value):
		self.store[key] = value

	def __iter__(self):
		return iter(self.store)


class Number:   

	def __init__(self, value):
		self.value = value

	def evaluate(self, scope):
		return self


class Function:

	def __init__(self, args, body):
		self.args = args
		self.body = body

	def evaluate(self, scope):
		res = None
		for f in self.body:
			res = f.evaluate(scope)
		return res


class FunctionCall:

	def __init__(self, fun_expr, args):
		self.fun_expr = fun_expr
		self.args = args

	def evaluate(self, scope):
		function = self.fun_expr.evaluate(scope)
		call_args = []
		for arg in self.args:
			call_args.append(arg.evaluate(scope))
		call_scope = Scope(scope)
		i = 0
		for arg in function.args:
			call_scope[arg] = call_args[i]
			i += 1
		return function.evaluate(call_scope)


class Reference:

	def __init__(self, name):
		self.name = name

	def evaluate(self, scope):
		return scope[self.name]


class FunctionDefinition:

	def __init__(self, name, function):
		self.name = name
		self.function = function

	def evaluate(self, scope):
		scope[self.name] = self.function
		return self.function


class UnaryOperation:
	def __init__(self, op, expr):
		self.op = op
		self.expr = expr

	def evaluate(self, scope):
		x = self.expr.evaluate(scope).value
		if self.op == '!':
			return Number(not x)
		else:
			return Number(-1 * x)


class BinaryOperation:
	def add(l, r):
		return l + r

	def sub(l, r):
		return l - r

	def mul(l, r):
		return l * r

	def div(l, r):
		return l // r

	def mod(l, r):
		return l % r

	def eq(l, r):
		return l == r

	def ne(l, r):
		return l != r

	def lt(l, r):
		return l < r

	def gt(l, r):
		return l > r

	def le(l, r):
		return l <= r

	def ge(l, r):
		return l >= r

	def land(l, r):
		return l and r

	def lor(l, r):
		return l or r

	operations = {
		'+': add,
		'-': sub,
		'*': mul,
		'/': div,
		'%': mod,
		'==': eq,
		'!=': ne,
		'<': lt,
		'>': gt,
		'<=': le,
		'>=': ge,
		'&&': land,
		'||': lor,
		}

	def __init__(self, lhs, op, rhs):
		self.lhs = lhs
		self.op = op
		self.rhs = rhs

	def evaluate(self, scope):
		l = self.lhs.evaluate(scope)
		r = self.rhs.evaluate(scope)
		return Number(self.operations[self.op](l.value, r.value))

class Print:

	def __init__(self, expr):
		self.expr = expr

	def evaluate(self, scope):
		num = self.expr.evaluate(scope)
		if num:
			print(num.value)
		return num

class Read:

	def __init__(self, name):
		self.name = name

	def evaluate(self, scope):
		scope[self.name] = Number(int(input()))
		return scope[self.name]

class Conditional:
	def __init__(self, condition, if_true, if_false = None):
		self.condition = condition
		self.if_true = if_true
		self.if_false = if_false

	def evaluate(self, scope):
		res = None
		cond = self.condition.evaluate(scope)
		if cond and cond.value:
			for f in self.if_true or []:
				res = f.evaluate(scope)  
		else:
			for f in self.if_false or []:
				res = f.evaluate(scope)
		return res

def example():
	parent = Scope()
	parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
	parent["bar"] = Number(10)
	scope = Scope(parent)
	assert 10 == scope["bar"].value
	scope["bar"] = Number(20)
	assert scope["bar"].value == 20
	print('It should print 2: ', end=' ')
	FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)

def new_test():
	fun = Function((), [Print(Conditional(Conditional(Number(0), [Print(Number(100))]
	),[Print(Number(1000))]))])
	scope = Scope()
	FunctionCall(FunctionDefinition('fun', fun), []).evaluate(scope)

def my_tests():
	fun1 = Function(('x', 'y', 'z'), [Print(BinaryOperation(BinaryOperation(Reference('x'), '*', Reference('y')),
	 '%', Reference('z')))])
	scope = Scope()      
	print('(5 * 3) % 4 =', end=' ')
	FunctionCall(FunctionDefinition('fun1', fun1), [Number(5), Number(3), Number(4)]).evaluate(scope)

	fun2 = Function(('x', 'y'), [Conditional(BinaryOperation(Reference('x'), '==', Reference('y')), [Print(Number(1))], [Print(Number(0))])])
	scope = Scope()      

	print('if 5 equals 5, then 1, else 0:', end=' ')

	FunctionCall(FunctionDefinition('fun2', fun2), [Number(5), Number(5)]).evaluate(scope)

	fun4 = Function((), [
		Read('x'), 
		Read('y'), 
		Conditional(
			BinaryOperation(Reference('x'), '>', Reference('y')), 
			[Print(Reference('x'))], 
			[Print(Reference('y'))])])
	scope1 = Scope()
	print('read 2 numbers, print greater')
	FunctionCall(FunctionDefinition('fun4', fun4), []).evaluate(scope1)


	fun3 = Function(('x', 'y', 'z'), [Conditional(
		BinaryOperation(
		BinaryOperation(Reference('x'), '==', Reference('y')),
		'||',
		BinaryOperation(Reference('x'), '==', Reference('z')),),
		 [Print(Number(123))])])
	scope1 = Scope()      

	print('if 5 equals 3 or 4, then 123, else nothing:', end=' ')

	FunctionCall(FunctionDefinition('fun3', fun3), [Number(5), Number(3), Number(4)]).evaluate(scope1)

def func_condition_read_test():
	print('Enter a, b, c')
	main = Scope()
	main['foo'] = Function(('enum', 'denom', 'val'),
	[
	Conditional(
	FunctionCall(Reference('check_answer'),
	[Reference('enum'),
	Reference('denom'),
	Reference('val')]),
	[
	Print(Reference('val'))
	],
	[
	Print(Number(-1))
	]
	)
	])
	main['check_answer'] = Function(('a', 'b', 'c'),
	[
	Conditional(
	BinaryOperation(Reference('c'),
	'==',
	BinaryOperation(Reference('a'),
	'+',
	Reference('b'))),
	[
	Number(1)
	],
	[
	Number(0)
	])
	])
	print('It would print c, if a + b = c and -1 if not: ', end=' ')
	assert FunctionCall(FunctionDefinition('foo', main['foo']),
	[
	Read('first'),
	Read('second'),
	Read('third')
	]).evaluate(main)
			
if __name__ == '__main__':
	#example()
	new_test()
	#my_tests()
	#func_condition_read_test()
