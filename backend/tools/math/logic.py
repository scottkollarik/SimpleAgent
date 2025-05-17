import ast
import operator
from typing import Callable

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod
}

def eval_expr(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(f"Unsupported expression: {type(node).__name__}")
    return _eval(ast.parse(expr, mode="eval").body)

def evaluate_expression(query: str, llm_helper: Callable[[str], str] = None) -> str:
    if llm_helper:
        prompt = f"""
You are a math-normalization assistant. Convert the following text into a clean mathematical expression using numbers and operators (+, -, *, /):

\"\"\"{query}\"\"\"
Only return the cleaned expression rewritten using numbers and operators. Do NOT evaluate it:
"""
        query = llm_helper(prompt).strip()

    try:
        result = eval_expr(query)
        return f"The result of the expression {query} is {result}."
    except Exception as e:
        return f"Sorry, I couldn't evaluate the expression. Error: {str(e)}"