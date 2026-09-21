from __future__ import annotations

import ast
import json
import operator
from typing import Callable

from langchain_core.tools import tool

from database import get_student, initialize_database

initialize_database()


def _json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False)


@tool
def get_student_info(student_id: str) -> str:
    """Get a student's name and department from a student ID such as 22CS045."""
    student = get_student(student_id)
    if student is None:
        return _json({"found": False, "student_id": student_id.strip().upper()})
    return _json(
        {
            "found": True,
            "student_id": student["student_id"],
            "name": student["name"],
            "department": student["department"],
        }
    )


@tool
def get_student_marks(student_id: str) -> str:
    """Get Python, Database, AI, and Web marks for a student ID such as 22CS045."""
    student = get_student(student_id)
    if student is None:
        return _json({"found": False, "student_id": student_id.strip().upper()})
    return _json(
        {
            "found": True,
            "student_id": student["student_id"],
            "python": student["python"],
            "database": student["database"],
            "ai": student["ai"],
            "web": student["web"],
        }
    )


_ALLOWED_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINARY_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_BINARY_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY_OPERATORS:
        return _ALLOWED_UNARY_OPERATORS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Only numeric arithmetic expressions are allowed.")


@tool
def calculator(expression: str) -> str:
    """Safely evaluate numeric arithmetic. Use this tool for totals, averages, percentages, and arithmetic derived from marks."""
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _safe_eval(parsed)
        if abs(result) > 1e12:
            raise ValueError("Result is too large.")
        clean_result: int | float
        if result.is_integer():
            clean_result = int(result)
        else:
            clean_result = round(result, 6)
        return _json({"expression": expression, "result": clean_result})
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as exc:
        return _json({"error": str(exc), "expression": expression})


@tool
def get_passing_rules() -> str:
    """Return the university passing rules: minimum overall average and minimum mark required in every subject."""
    return _json(
        {
            "minimum_overall_average_percent": 40,
            "minimum_mark_each_subject": 35,
        }
    )


TOOLS = [get_student_info, get_student_marks, calculator, get_passing_rules]
