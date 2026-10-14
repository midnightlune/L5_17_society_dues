import sqlite3
import operator
import ast

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE dues (flat TEXT, month TEXT, amount INTEGER, paid INTEGER)")

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def add_due(flat, month, amount, history=None):
    if history is None:
        history = []
    conn.execute("INSERT INTO dues VALUES (?, ?, ?, 0)", (flat, month, amount))
    history.append((flat, month))
    return history

def collect(flat, month):
    row = conn.execute("SELECT amount FROM dues WHERE flat = ? AND month = ?", (flat, month)).fetchone()
    if row is None:
        return None
    conn.execute("UPDATE dues SET paid = 1 WHERE flat = ? AND month = ?", (flat, month))
    return row[0]

def _evaluate(node):
    # new function added to safely evaluate a parsed arithmetic function
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    
    raise ValueError("unsupported expression")

def penalty(rule):
    try:
        return _evaluate(ast.parse(rule, mode="eval"))
    except (ValueError, SyntaxError, ZeroDivisionError):
        return 0

def pending():
    rows = conn.execute("SELECT flat FROM dues WHERE paid = 0").fetchall()
    return [r[0] for r in rows]

def main():
    add_due("A-101", "Oct", 2500)
    add_due("A-102", "Oct", 2500)
    print(collect("A-101", "Oct"))
    print(penalty("50 * 2"))
    print(pending())


main()
