from lisp import *

def repl(prompt='lis.py> '):
    while True:
        val = eval(parse(input(prompt)))
        if val is not None: 
            print(schemestr(val))

def schemestr(exp):
    if isinstance(exp, list):
        return '(' + ' '.join(map(schemestr, exp)) + ')' 
    else:
        return str(exp)

repl()