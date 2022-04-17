import math
import operator as op
from pprint import pprint

def tokenize(s):
    return (s
        .replace("(", " ( ")
        .replace(")", " ) ")
        .split())

def read(ts):
    if len(ts) == 0:
        raise SyntaxError('unexpected EOF')
    t = ts.pop(0)
    if t == "(":
        l = []
        while ts[0] != ")":
            l.append(read(ts))
        ts.pop(0)
        return l
    elif t == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(t)

def atom(t):
    try: return int(t)
    except ValueError:
        try: return float(t)
        except ValueError:
            return str(t)

def parse(s):
    return read(tokenize(s))

def build_default_env():
    "An environment with some Scheme standard procedures."
    env = {}
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'expt':    pow,
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x, list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: (),  
		'print':   print,
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, str),
    })
    return env

DEBUG = True
DEFAULT_ENV = build_default_env()

def eval(exp, env=DEFAULT_ENV):
    if DEBUG:
        print(exp)
    if isinstance(exp, str):
        if DEBUG:
            val = env[exp]
            print(f"str: {exp} = {val}")
        return val
    elif isinstance(exp, (int, float)):
        return exp
    elif exp[0] == "if":
        _just_the_word_if_, test, conseq, default = exp
        exp2 = conseq if test else default
        return eval(exp2, env)
    elif exp[0] == "define":
        _just_the_word_define_, name, sub_exp = exp
        env[name] = eval(sub_exp, env)
    else:   #   variadic function call
        proc = eval(exp[0], env)
        args = [eval(arg, env) for arg in exp[1:]]
        return proc(*args)

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

if __name__ == "__main__":
    code = """
            (begin 
                (define r 10)
                (* pi (* r r))
            )
            """
    ast = parse(code)
    pprint(ast)
    print(eval(ast))
    #repl()
