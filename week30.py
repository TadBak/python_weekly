def betterrepr(cls):
    class Inner(cls):
        def __repr__(self):
            return (f'Instance of {self.__class__.__bases__[0].__name__}, '
                    f'vars = {self.__dict__}')
    return Inner

@betterrepr
class Foo:
    def __init__(self, x, y):
        self.x = x
        self.y = y


f = Foo(10, [1, 2, 3, 4, 5])
print(f)

