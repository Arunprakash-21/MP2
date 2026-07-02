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
