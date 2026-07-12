from library import Stack, EvaluateExpression


def test_stack_push_pop_peek():
    stack = Stack()
    assert stack.is_empty
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert len(stack) == 3
    assert stack.peek() == 3
    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.peek() == 1
    assert not stack.is_empty


def test_stack_empty_returns_none():
    stack = Stack()
    assert stack.pop() is None
    assert stack.peek() is None
    assert len(stack) == 0


def test_expression_property():
    evaluator = EvaluateExpression()
    assert evaluator.expression == ""
    evaluator.expression = "1 + 2"
    assert evaluator.expression == "1 + 2"
    evaluator.expression = "1 + a"  # invalid characters are rejected
    assert evaluator.expression == ""
    assert EvaluateExpression("(1+2)*3").insert_space() == " ( 1 + 2 )  * 3"


def test_evaluate():
    assert EvaluateExpression("1 + 2").evaluate() == 3
    assert EvaluateExpression("1 + 2 * 3").evaluate() == 7
    assert EvaluateExpression("(1 + 2) * 3").evaluate() == 9
    assert EvaluateExpression("(1 + 2) * 4 - 3").evaluate() == 9
    assert EvaluateExpression("(6 + 2) / 4").evaluate() == 2
    assert EvaluateExpression("((1 + 2) * 3 - 4) / 5 + 10").evaluate() == 11


def test_evaluate_negative_numbers():
    assert EvaluateExpression("-4 + 5").evaluate() == 1
    assert EvaluateExpression("3 + -2").evaluate() == 1
    assert EvaluateExpression("2 * -3").evaluate() == -6
    assert EvaluateExpression("(-4)").evaluate() == -4
    assert EvaluateExpression("-2 * -3").evaluate() == 6


def test_evaluate_floats():
    assert EvaluateExpression("1.5 + 2").evaluate() == 3.5
    assert EvaluateExpression("7 / 2").evaluate() == 3.5
    assert EvaluateExpression("10 / 4").evaluate() == 2.5
    assert EvaluateExpression("0.5 * 4").evaluate() == 2


def test_evaluate_unbalanced_brackets_returns_none():
    assert EvaluateExpression("(1 + 2").evaluate() is None
    assert EvaluateExpression("1 + 2)").evaluate() is None
