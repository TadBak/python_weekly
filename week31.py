from functools import wraps

def betterrepr(newstr=None, newrepr=None):

    def decorator(cls):
        """Decorator docstring"""

        def myrepr(self):
            return f'Instance of {self.__class__.__name__}, vars = {vars(self)}'
            
        cls.__repr__ = newrepr if newrepr and callable(newrepr) else myrepr
        if newstr and callable(newstr):
            cls.__str__ = newstr

        @wraps(cls)
        def wrapper(*args, **kwargs):
            """Wrapper docstring"""
            return cls(*args, **kwargs)

        return wrapper

    return decorator

# ----- testing below -----

def repr_test(self):
    return 'Custom __repr__ string'

def str_test(self):
    return 'Custom __str__ string'

@betterrepr()
class Foo:
    """Class Foo docstring"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

@betterrepr(str_test)
class Bar:
    """Class Bar docstring"""
    pass

@betterrepr(newrepr=repr_test)
class Baz:
    """Class Baz docstring"""
    pass

f = Foo(10, [1,2,3,4,5])
print(f)
print(Foo.__doc__)
br = Bar()
print(br)
print(Bar.__doc__)
bz = Baz()
print(bz)
print(Baz.__doc__)

