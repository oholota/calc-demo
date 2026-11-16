"""Safe arithmetic for the calculator.

Never pass user input to eval(): eval("__import__('os').system('...')") runs
any code the user sends. Instead the expression is parsed into a syntax tree
and only numbers, + - * / and parentheses are allowed.
"""
import ast
import math
import operator

MAX_LENGTH = 200

_BINARY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalcError(ValueError):
    """The expression cannot be calculated."""


def evaluate(expression):
    """Return the value of an arithmetic expression such as "2 + 3 * (4 - 1)"."""
    expression = str(expression).strip()
    if not expression:
        raise CalcError("Empty expression")
    if len(expression) > MAX_LENGTH:
        raise CalcError(f"Expression is longer than {MAX_LENGTH} characters")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise CalcError("Invalid expression") from None
    try:
        result = _eval(tree.body)
    except OverflowError:
        raise CalcError("Result is too large") from None
    if isinstance(result, float):
        if not math.isfinite(result):
            raise CalcError("Result is too large")
        if result.is_integer():
            return int(result)
        return round(result, 10)
    return result


def _eval(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
        left = _eval(node.left)
        right = _eval(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise CalcError("Division by zero")
        return _BINARY[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    raise CalcError("Only numbers, + - * / and parentheses are allowed")
