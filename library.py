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

    valid_char = "0123456789.+-*/() "
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

    def is_number(self, token):
        # True if the token is a number (may be signed or have a decimal).
        try:
            float(token)
            return True
        except ValueError:
            return False

    def to_number(self, token):
        # Convert a number token to an int when whole, otherwise a float.
        if "." in token:
            return float(token)
        return int(token)

    def merge_signs(self, tokens):
        # Turn a unary +/- (a sign, not subtraction) into part of the number
        # that follows it, e.g. ['2', '*', '-', '3'] -> ['2', '*', '-3'].
        # A +/- is unary when it starts the expression or follows another
        # operator or an opening bracket.
        merged = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            is_sign = token in "+-"
            unary_position = not merged or merged[-1] in "+-*/("
            has_next_number = (i + 1 < len(tokens)
                               and self.is_number(tokens[i + 1]))
            if is_sign and unary_position and has_next_number:
                merged.append(token + tokens[i + 1])
                i += 2
            else:
                merged.append(token)
                i += 1
        return merged

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
            result = left / right
        operand_stack.push(result)

    def evaluate(self):
        # Evaluate the infix expression. Returns an int when the result is a
        # whole number, otherwise a float; returns None for an empty
        # expression or one with unbalanced brackets.
        operand_stack = Stack()
        operator_stack = Stack()
        tokens = self.merge_signs(self.insert_space().split())

        for token in tokens:
            if self.is_number(token):
                operand_stack.push(self.to_number(token))
            elif token in "+-":
                while (not operator_stack.is_empty
                       and operator_stack.peek() != "("):
                    self.process_operator(operand_stack, operator_stack)
                operator_stack.push(token)
            elif token in "*/":
                while (not operator_stack.is_empty
                       and operator_stack.peek() != "("
                       and self.precedence[operator_stack.peek()]
                       >= self.precedence[token]):
                    self.process_operator(operand_stack, operator_stack)
                operator_stack.push(token)
            elif token == "(":
                operator_stack.push(token)
            elif token == ")":
                while (not operator_stack.is_empty
                       and operator_stack.peek() != "("):
                    self.process_operator(operand_stack, operator_stack)
                if operator_stack.is_empty:
                    return None  # unmatched ')'
                operator_stack.pop()

        while not operator_stack.is_empty:
            if operator_stack.peek() == "(":
                return None  # unmatched '('
            self.process_operator(operand_stack, operator_stack)

        result = operand_stack.pop()
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result
