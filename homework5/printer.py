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
        prev_state = self.is_sentence
        self_is_sentence = True
        self.indent += 1
        for sentence in fdef.function.body:
            sentence.visit(self)
        self.indent -= 1
        self.is_sentence = prev_state
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

    def visitConditional(self, cond):
        print("\t" * self.indent + "if (", end="")
        self.is_sentence = False
        cond.condition.visit(self)
        self.is_sentence = True

        print(") {")
        self.indent += 1
        if cond.if_true:
            for sentence in cond.if_true:
                sentence.visit(self)

        if cond.if_false:
            print("\t" * (self.indent - 1) + "} else {")
            for sentence in cond.if_false:
                sentence.visit(self)

        self.indent -= 1
        print("\t" * self.indent + "};")