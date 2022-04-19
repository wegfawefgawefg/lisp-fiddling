import math
import operator as op
from pprint import pprint
import colorama

colors = [
    colorama.Fore.WHITE,
    colorama.Fore.RED,
    colorama.Fore.GREEN,
    colorama.Fore.YELLOW,
    colorama.Fore.BLUE,
    colorama.Fore.MAGENTA,
    colorama.Fore.CYAN,
]

def tokenize(s):
    return (f"(begin {s} )"
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

class Env(dict):
    '''refer to parent dicts on key miss,
        can result in recursively jumping to respective parents, 
            if miss all the way to root will return None'''
    def __init__(self, keys_=(), vals=(), parent=None):
        self.update(zip(keys_, vals))
        self.parent = parent

    def find(self, key):
        return self if (key in self) else self.parent.find(key)

class Procedure:
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        return eval(self.body, Env(keys_=self.params, vals=args, parent=self.env))


def build_default_env():
    "An environment with some Scheme standard procedures."
    env = Env()
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
        'number?': lambda x: isinstance(x, (int, float)),  
		'print':   print,
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, str),
    })
    return env

DEBUG = True
DEFAULT_ENV = build_default_env()

def eval(exp, env=DEFAULT_ENV, depth=0):
    if DEBUG:
        print(
            colors[depth % len(colors)] +
            '  ' * depth + schemestr(exp))
    if isinstance(exp, str): # variable to lookup or procedure to evaluate
        var = env.find(exp)[exp]
        if DEBUG:
            print(
                colors[(depth + 1) % len(colors)] +
                '  ' * (depth + 1) + schemestr(var))
        return var
    elif not isinstance(exp, list): # a constant of some type, that is not in the env
        return exp

    op, *args = exp
    if op == 'quote':
        return args[0]
    elif op == 'if':
        test, conseq, default = args
        exp2 = conseq if eval(test, env, depth=depth+1) else default
        return eval(exp2, env, depth=depth+1)
    elif op == 'define':
        name, sub_exp = args
        env[name] = eval(sub_exp, env, depth=depth+1)
    elif op == 'set!': # (metadefine) like define but in as high an env as possible
        symbol, exp2 = args
        env.find(symbol)[symbol] = eval(exp2, env, depth=depth+1)
    elif op == 'lambda':
        params, body = args
        return Procedure(params, body, env)
    else:   # procedure call
        proc = eval(op, env, depth=depth+1) 
        its_args = [eval(arg, env, depth=depth+1) for arg in args]
        return proc(*its_args)

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
    code = '''
        (define r 10)
        (* pi (* r r))
        (define circle-area (lambda (r) (* pi (* r r))))
        (define area (circle-area 10))
        (print area)
    '''
    code = '''
        (define make-account
            (lambda (balance)
                (lambda (amt)
                    (begin (set! balance (+ balance amt))
                    balance))))
        (define account1 (make-account 100.00))
        (account1 -20.00)
    '''
    ast = parse(code)
    #pprint(ast)
    print(eval(ast))
    
    print(colorama.Fore.RESET, colorama.Style.RESET_ALL)    #   reset term colors
    #repl()
