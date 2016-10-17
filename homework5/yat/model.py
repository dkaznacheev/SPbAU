class Scope():
    def __init__(self, parent=None):
        self.store = {}
        self.parent = parent

    def __getitem__(self, key):
        if key in self.store:
            return self.store[key]
        if self.parent:
            return self.parent[key]
        return None

    def __setitem__(self, key, value):
        self.store[key] = value

    def __iter__(self):
        return iter(self.store)


class Number:
    def __init__(self, value):
        self.value = value

    def visit(self, visitor):
        visitor.visitNumber(self)

    def fold(self, folder):
        return folder.foldNumber(self)

    def evaluate(self, scope):
        return self


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def fold(self, folder):
        return folder.foldFunction(self)

    def evaluate(self, scope):
        res = None
        for f in self.body:
            res = f.evaluate(scope)
        return res


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def fold(self, folder):
        return folder.foldFunctionCall(self)

    def visit(self, visitor):
        visitor.visitFunctionCall(self)

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        call_scope.store.update(zip(function.args, [arg.evaluate(scope) for arg in self.args]))
        return function.evaluate(call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def fold(self, folder):
        return folder.foldReference(self)

    def visit(self, visitor):
        visitor.visitReference(self)

    def evaluate(self, scope):
        return scope[self.name]


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def fold(self, folder):
        return folder.foldFunctionDefinition(self)

    def visit(self, visitor):
        visitor.visitFunctionDefinition(self)

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def visit(self, visitor):
        visitor.visitUnaryOperation(self)

    def fold(self, folder):
        return folder.foldUnaryOperation(self)

    def evaluate(self, scope):
        x = self.expr.evaluate(scope).value
        if self.op == '!':
            return Number(int(not x))
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

    def fold(self, folder):
        return folder.foldBinaryOperation(self)

    def visit(self, visitor):
        visitor.visitBinaryOperation(self)

    def evaluate(self, scope):
        l = self.lhs.evaluate(scope)
        r = self.rhs.evaluate(scope)
        return Number(int(self.operations[self.op](l.value, r.value)))


class Print:
    def __init__(self, expr):
        self.expr = expr

    def fold(self, folder):
        return folder.foldPrint(self)

    def visit(self, visitor):
        visitor.visitPrint(self)

    def evaluate(self, scope):
        num = self.expr.evaluate(scope)
        print(num.value)
        return num


class Read:
    def __init__(self, name):
        self.name = name

    def fold(self, folder):
        return folder.foldRead(self)

    def visit(self, visitor):
        visitor.visitRead(self)

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))
        return scope[self.name]


class Conditional:
    def __init__(self, condition, if_true = None, if_false = None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def fold(self, folder):
        return folder.foldConditional(self)

    def visit(self, visitor):
        visitor.visitConditional(self)

    def evaluate(self, scope):
        res = None
        branch = None
        if self.condition.evaluate(scope).value and self.if_true:
            branch = self.if_true
        elif self.if_false:
            branch = self.if_false
        if branch:
            for f in branch:
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
    fun = Function((), [Conditional(Number(0), [Print(Number(1000))])])
    scope = Scope()
    FunctionCall(FunctionDefinition('fun', fun), []).evaluate(scope)


def new_test1():
    scope = Scope()

    fun1 = Function(('x'), [Print(Reference('x'))])
    fun2 = Function(('x'), [FunctionCall(FunctionDefinition('fun1', fun1), [Reference('x')])])
    FunctionCall(FunctionDefinition('fun2', fun2), [Number(200)]).evaluate(scope)


def my_tests():
    fun1 = Function(('x', 'y', 'z'), [Print(BinaryOperation(BinaryOperation(Reference('x'), '*', Reference('y')),
                                                            '%', Reference('z')))])
    scope = Scope()
    print('(5 * 3) % 4 =', end=' ')
    FunctionCall(FunctionDefinition('fun1', fun1), [Number(5), Number(3), Number(4)]).evaluate(scope)

    fun2 = Function(('x', 'y'), [
        Conditional(BinaryOperation(Reference('x'), '==', Reference('y')), [Print(Number(1))], [Print(Number(0))])])
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
            BinaryOperation(Reference('x'), '==', Reference('z')), ),
        [Print(Number(123))])])
    scope1 = Scope()

    print('if 5 equals 3 or 4, then 123, else nothing:', end=' ')

    FunctionCall(FunctionDefinition('fun3', fun3), [Number(5), Number(3), Number(4)]).evaluate(scope1)


def test():
    Conditional(UnaryOperation('!', Number(0))).evaluate(Scope())

if __name__ == '__main__':
    # example()
    # new_test()
    # new_test1()
    # my_tests()     
    pass