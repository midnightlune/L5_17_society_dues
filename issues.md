# Issues Found in `society_dues.py`

Line numbers refer to the original file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Use of `eval()` on input (B307 / W0123) | Security (Medium, High confidence) | 21 | `penalty()` runs `eval(rule)`, so any string passed in can execute arbitrary Python code. | Parse with `ast.parse` and evaluate only numeric constants and `+ - * /` using a whitelist of operators. |
| SQL injection via f-string (B608) | Security (Medium) | 9 | `addDue` builds the INSERT by inserting `flat` and `month` directly into the SQL, so a value like `x'); DROP TABLE dues;--` alters the query. | Use a parameterised query: `INSERT INTO dues VALUES (?, ?, ?, 0)`. |
| Mutable default argument (W0102) | Bug | 8 | `history=[]` is created once and shared across all calls, so history leaks between unrelated calls. | Default to `None` and create a new list inside the function. |
| Hardcoded password (B105) | Security (Low) | 5 | `TREASURER_PASSWORD = "flat#101"` is stored in source code (and is unused). | Removed it; secrets should come from environment variables or a secrets manager if needed. |
| Broad exception (W0718) | Bug / Quality | 22 | `except Exception` hides every error, including programming mistakes. | Catch only `ValueError`, `SyntaxError` and `ZeroDivisionError`. |
| Inconsistent return (R1710) | Bug / Quality | 12-16 | `collect()` returns an amount when found but falls off the end (implicit `None`) otherwise. | Return `None` explicitly using an early return when no row is found. |
| Comparison to `None` with `!=` (E711 / C0121) | Style / Bug | 29 | `rows != None` is non-idiomatic, and `fetchall()` never returns `None`, so the check is pointless. | Removed the check; `fetchall()` returns a list, so the comprehension handles the empty case. |
| Function naming (C0103) | Style | 8 | `addDue` is camelCase, not snake_case. | Renamed to `add_due` and updated the callers. |
| Missing docstrings (C0114 / C0116) | Style | 1, 8, 12, 19, 27, 34 | Module and all functions lack docstrings. | Added a docstring to the module and every function. |
| Line too long (E501 / C0301) | Style | 4, 13, 15 | Lines exceed 79 characters. | Wrapped long calls across lines. |
| Missing blank lines (E302) | Style | 12 | `collect` needs two blank lines before it. | Added the blank lines. |
| Top-level `main()` call | Design | 41 | The demo runs automatically on import. | Wrapped in `if __name__ == "__main__":`. |

## Verification

After the fixes: Pylint **10.00/10**, Flake8 reports nothing, Bandit reports 0 issues. The program still prints `2500`, `100`, `['A-102']`.
