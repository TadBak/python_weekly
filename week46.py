
# decorator function
def mymypy(types):
    def wrap(func):
        def inner(*args):
            for t, a in zip(types, args):
                if not isinstance(a, t):
                    raise TypeError(f'Argument: {a} is not type {t}')
            return func(*args)
        return inner
    return wrap

# --- testing ---

@mymypy([float, int])
def mul(a, b):
    return a * b

try:
    print(f'mul result: {mul(2.5, 3)}')
    print(f'mul result: {mul(4, 2)}')
except TypeError as e:
    print(e)


class MyClass:
    def __init__(self, x):
        self.x = x

@mymypy([int, MyClass, int])
def objtest(a, b, c):
    return a * b.x - c

mc = MyClass(5)

try:
    print(f'objtest result: {objtest(2, mc, 1)}')
    print(f'objtest result: {objtest(2, "k", 1)}')
except TypeError as e:
    print(e)

