from yat.model import Number, FunctionCall, Reference, FunctionDefinition, \
    Function, UnaryOperation, BinaryOperation, Print, Read, Conditional


class PrettyPrinter:
    def __init__(self):
        self.indent = 0

    def visit(self, expr):
        expr.visit(self)
        print(";")

    def visitNumber(self, number):            
        print(number.value, end="")
    
    def visitReference(self, reference):     
        print(reference.name, end="")  

    def visitFunctionCall(self, fcall):
        fcall.fun_expr.visit(self)
        print("(", end="")
        for i in range(len(fcall.args)):
            fcall.args[i].visit(self)
            if i != len(fcall.args) - 1:
                print(', ', end = "")
        print(")", end="")          

    def visitBody(self, body):
        self.indent += 1
        for sentence in body:
            print("\t" * self.indent, end = "")
            sentence.visit(self)
            print(';')
        self.indent -= 1
        
    def visitFunctionDefinition(self, fdef): 
        print("def " + fdef.name + "(", end="")
        print(", ".join(fdef.function.args) + ") {")
        self.visitBody(fdef.function.body)
        print("\t" * self.indent + "}", end="")

    def visitUnaryOperation(self, unop):
        print("(" + unop.op, end="")
        unop.expr.visit(self)        
        print(")", end="")

    def visitBinaryOperation(self, binop):
        print("(", end="")
        binop.lhs.visit(self)
        print(") " + binop.op + " (", end="")
        binop.rhs.visit(self)
        print(")", end="")       

    def visitPrint(self, printer):
        print("print ", end = "")
        printer.expr.visit(self)  

    def visitRead(self, reader):
        print("read " + reader.name, end = "")
        
    def visitConditional(self, cond):
        print("if (", end="")
        cond.condition.visit(self)
        print(") {")    
        if cond.if_true:
            self.visitBody(cond.if_true)
        if cond.if_false:
            print("\t" * (self.indent) + "} else {")
            self.visitBody(cond.if_false)
        print("\t" * self.indent + "}", end = "")

def test():
    f1 = Conditional(FunctionCall(Reference('x'), [Number(22)]), [Conditional(BinaryOperation(Number(0), '-', Number(6)), [],[Conditional(Number(0), [Conditional(UnaryOperation('-', Number(20)), [],[FunctionDefinition('foobar', Function(['ab', 'cd'], [
    Print(BinaryOperation(UnaryOperation('-', Number(120)), '*', BinaryOperation(UnaryOperation('-', Number(20)), '+', Reference('z')))), Read('x')
    ]))])],[])])],[Conditional(Number(0), [Conditional(Number(0), [],[Read('xxx')])],[])])

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
