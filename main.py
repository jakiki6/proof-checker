from lexer import lex
from check import check

text = """
% test uwu
% another comment line
(stmt (eq (imp A B) (or (not A) B))
    (truth (eq (imp A B) (or (not A) B))))
"""

truth, err = check(lex(text))
if truth:
    print("True")
else:
    print("False")
    print("Error was:", err)
