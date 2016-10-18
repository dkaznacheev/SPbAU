from yat.model import Number, FunctionCall, Reference, FunctionDefinition,\
Function, UnaryOperation, BinaryOperation, Print, Read, Conditional, Scope

class ConstantFolder:


    def visit(self, expr):
        return expr.visit(self)

    def visitNumber(self, number):
        return number

    def visitFunctionCall(self, fcall):
        fun_expr = fcall.fun_expr.visit(self)
        args = [arg.visit(self) for arg in fcall.args]
        return FunctionCall(fun_expr, args)

    def visitReference(self, ref):
        return ref

    def visitFunctionDefinition(self, fdef):
        return FunctionDefinition(fdef.name, fdef.function.visit(self))

    def visitFunction(self, fun):
        body = [f.visit(self) for f in fun.body]
        return Function(fun.args, body)

    def visitUnaryOperation(self, unop):
        expr = unop.expr.visit(self)
        if type(expr) is Number:
            return unop.evaluate(Scope())
        return UnaryOperation(unop.op, expr)

    def visitBinaryOperation(self, binop):
        lhs = binop.lhs.visit(self)
        rhs = binop.rhs.visit(self)
        if type(lhs) is Number and type(lhs) is Number:
            return binop.evaluate(Scope())
        if ((type(lhs) is Number and lhs.value == 0) or (type(rhs) is Number and rhs.value == 0)) and binop.op == '*':
            return Number(0)
        if type(lhs) is Reference and type(rhs) is Reference and lhs.name == rhs.name and binop.op == '-':
            return Number(0)
        return BinaryOperation(lhs, binop.op, rhs)
        
    def visitPrint(self, printer):
        return Print(printer.expr.visit(self))
    
    def visitRead(self, reader):
        return reader

    def visitConditional(self, cond):
        condition = cond.condition.visit(self)
        if_true = None
        if_false = None
        if cond.if_true:
            if_true = [f.visit(self) for f in cond.if_true]
        if cond.if_false:    
            if_false = [f.visit(self) for f in cond.if_false]
        return Conditional(condition, if_true, if_false)

cf = ConstantFolder()
nn = BinaryOperation(Number(5), '>=', Number(3))
n = nn.visit(cf)
print(n.value)