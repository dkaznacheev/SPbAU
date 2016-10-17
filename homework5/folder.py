from yat.model import Number, FunctionCall, Reference, FunctionDefinition,\
Function, UnaryOperation, BinaryOperation, Print, Read, Conditional, Scope

from printer import PrettyPrinter

class ConstantFolder:


    def fold(self, expr):
        return expr.visit(self)

    def foldNumber(self, number):
        return number

    def foldFunctionCall(self, fcall):
        fun_expr = fcall.fun_expr.fold(self)
        args = [arg.fold(self) for arg in fcall.args]
        return FunctionCall(fun_expr, args)

    def foldReference(self, ref):
        return ref

    def foldFunctionDefinition(self, fdef):
        return FunctionDefinition(fdef.name, fdef.function.fold(self))

    def foldFunction(self, fun):
        body = [f.fold(self) for f in fun.body]
        return Function(fun.args, body)

    def foldUnaryOperation(self, unop):
        expr = unop.expr.fold(self)
        if type(expr) is Number:
            return unop.evaluate(Scope())
        return UnaryOperation(unop.op, expr)

    def foldBinaryOperation(self, binop):
        lhs = binop.lhs.fold(self)
        rhs = binop.rhs.fold(self)
        if type(lhs) is Number and type(lhs) is Number:
            return binop.evaluate(Scope())
        if ((type(lhs) is Number and lhs.value == 0) or (type(rhs) is Number and rhs.value == 0)) and binop.op == '*':
            return Number(0)
        if type(lhs) is Reference and type(rhs) is Reference and lhs.name == rhs.name and binop.op == '-':
            return Number(0)
        return BinaryOperation(lhs, binop.op, rhs)
        
    def foldPrint(self, printer):
        return Print(printer.expr.fold(self))
    
    def foldRead(self, reader):
        return reader

    def foldConditional(self, cond):
        condition = cond.condition.fold(self)
        if_true = None
        if_false = None
        if cond.if_true:
            if_true = [f.fold(self) for f in cond.if_true]
        if cond.if_false:    
            if_false = [f.fold(self) for f in cond.if_false]
        return Conditional(condition, if_true, if_false)