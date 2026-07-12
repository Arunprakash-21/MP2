# A Stack implemented from Week 4 OOP Problem Set
class Stack:

    def __init__(self):
        self.__items = []

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        if self.__items:
            return self.__items.pop()
        return None

    def peek(self):
        if self.__items:
            return self.__items[-1]
        return None

    @property
    def is_empty(self):
        return len(self.__items) == 0

    @property
    def size(self):
        return len(self.__items)

    def __len__(self):
        return len(self.__items)


# Evaluates a math expression written in infix notation.
# Uses two Stacks (operands and operators) and operator precedence
# to compute the result, e.g. EvaluateExpression("(1 + 2) * 3").evaluate() == 9.
class EvaluateExpression:

    valid_char = "0123456789+-*/() "
    operators = "+-*/()"
    precedence = {"(": 1, "+": 2, "-": 2, "*": 3, "/": 3}

    def __init__(self, string=""):
        if isinstance(string, str) and self.is_valid(string):
            self._expression = string
        else:
            self._expression = ""

    def is_valid(self, string):
        # True only if every character is an allowed character.
        for char in string:
            if char not in self.valid_char:
                return False
        return True

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, new_expr):
        if new_expr and self.is_valid(new_expr):
            self._expression = new_expr
        else:
            self._expression = ""

    def insert_space(self):
        # Return the expression with every operator padded by spaces.
        result = ""
        for char in self._expression:
            if char in self.operators:
                result += f" {char} "
            else:
                result += char
        return result

    def process_operator(self, operand_stack, operator_stack):
        # Pop one operator and two operands, apply the operator,
        # and push the result back onto the operand stack.
        operator = operator_stack.pop()
        right = operand_stack.pop()
        left = operand_stack.pop()
        if operator == "+":
            result = left + right
        elif operator == "-":
            result = left - right
        elif operator == "*":
            result = left * right
        elif operator == "/":
            result = left // right
        operand_stack.push(result)

    def evaluate(self):
        # Evaluate the infix expression and return the result as an int.
        operand_stack = Stack()
        operator_stack = Stack()
        expression = self.insert_space()
        tokens = expression.split()

        for token in tokens:
            if token.isdigit():
                operand_stack.push(int(token))
            elif token in "+-":
                while (not operator_stack.is_empty
                       and operator_stack.peek() != "("):
                    self.process_operator(operand_stack, operator_stack)
                operator_stack.push(token)
            elif token in "*/":
                while (not operator_stack.is_empty
                       and self.precedence[operator_stack.peek()]
                       >= self.precedence[token]):
                    self.process_operator(operand_stack, operator_stack)
                operator_stack.push(token)
            elif token == "(":
                operator_stack.push(token)
            elif token == ")":
                while operator_stack.peek() != "(":
                    self.process_operator(operand_stack, operator_stack)
                operator_stack.pop()

        while not operator_stack.is_empty:
            self.process_operator(operand_stack, operator_stack)

        return operand_stack.pop()
