from yat.model import Number, FunctionCall, Reference, FunctionDefinition, \
    Function, UnaryOperation, BinaryOperation, Print, Read, Conditional


class PrettyPrinter:
    def __init__(self):
        self.indent = 0
        self.is_sentence = True

    def visit(self, expr):
        expr.visit(self)

    def visitNumber(self, number):
        if self.is_sentence:
            print("\t" * self.indent, end="")
        print(number.value, end="")
        if self.is_sentence:
            print(";")

    def visitReference(self, reference):
        if self.is_sentence:
            print("\t" * self.indent, end="")
        print(reference.name, end="")
        if self.is_sentence:
            print(";")

    def visitFunctionCall(self, fcall):
        if self.is_sentence:
            print("\t" * self.indent, end="")
        prev_state = self.is_sentence
        self.is_sentence = False
        fcall.fun_expr.visit(self)
        print("(", end="")
        for i in range(len(fcall.args)):
            fcall.args[i].visit(self)
            if i != len(fcall.args) - 1:
                print(', ', end = "")
        print(")", end="")
        self.is_sentence = prev_state
        if self.is_sentence:
            print(";")

    def visitFunctionDefinition(self, fdef):
        if self.is_sentence:
            print("\t" * self.indent, end="")
        print("def " + fdef.name + "(", end="")
        print(", ".join(fdef.function.args) + ") {")
        self.indent += 1
        for sentence in fdef.function.body:
            sentence.visit(self)
        self.indent -= 1
        print("\t" * self.indent + "}", end="")
        if self.is_sentence:
            print(";")

    def visitUnaryOperation(self, unop):
        if self.is_sentence:
            print("\t" * self.indent, end="")
        print("(" + unop.op, end="")

        prev_state = self.is_sentence
        self.is_sentence = False
        unop.expr.visit(self)
        self.is_sentence = prev_state

        print(")", end="")

        if self.is_sentence:
            print(";")

    def visitBinaryOperation(self, binop):
        if self.is_sentence:
            print("\t" * self.indent, end="")

        prev_state = self.is_sentence
        self.is_sentence = False
        print("(", end="")
        binop.lhs.visit(self)
        print(") " + binop.op + " (", end="")
        binop.rhs.visit(self)
        print(")", end="")
        self.is_sentence = prev_state

        if self.is_sentence:
            print(";")

    def visitPrint(self, printer):
        print("\t" * self.indent + "print ", end="")

        self.is_sentence = False
        printer.expr.visit(self)
        self.is_sentence = True

        print(";")

    def visitRead(self, reader):
        print("\t" * self.indent + "read " + reader.name + ";")

    def visitBranch(self, branch):
        for sentence in branch:
            sentence.visit(self)
        
    def visitConditional(self, cond):
        print("\t" * self.indent + "if (", end="")
        self.is_sentence = False
        cond.condition.visit(self)
        self.is_sentence = True

        print(") {")
        self.indent += 1
        if cond.if_true:
            self.visitBranch(cond.if_true)
        if cond.if_false:
            print("\t" * (self.indent - 1) + "} else {")
            self.visitBranch(cond.if_false)
        self.indent -= 1
        print("\t" * self.indent + "};")

def test():
    f1 = Conditional(FunctionCall(Reference('x'), [Number(22)]), [Conditional(BinaryOperation(Number(0), '-', Number(6)), [],[Conditional(Number(0), [Conditional(UnaryOperation('-', Number(20)), [],[FunctionDefinition('foobar', Function(['ab', 'cd'], [
    Print(BinaryOperation(UnaryOperation('-', Number(120)), '*', BinaryOperation(UnaryOperation('-', Number(20)), '+', Reference('z')))), Read('x')
    ]))])],[])])],[Conditional(Number(0), [Conditional(Number(0), [],[])],[])])

    f = FunctionDefinition('foo', Function(['a', 'b'], [
    FunctionDefinition('bar', Function(['c', 'd'], [
    Read('c')
    ])),
    Conditional(Number(6), [Conditional(Number(5), [Read('x')])],[f1])
    ]))

    pr = PrettyPrinter()
    pr.visit(f)

if __name__ == '__main__':
	test()               
