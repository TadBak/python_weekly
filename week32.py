class PercentageTooHighError(Exception):
    pass


class PercentageTooLowError(Exception):
    pass


class Percentage:

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        v = int(value)  # exception will be thrown if value is not a number
        if v < 0:
            raise PercentageTooLowError
        if v > 100:
            raise PercentageTooHighError
        instance.__dict__[self.name] = v

    def __set_name__(self, owner, name):
        self.name = name


class Foo:   
    participation = Percentage()


# ---- tests ----
f1 = Foo()
f1.participation = 30
f2 = Foo()
f2.participation = 70
print(f1.participation) # prints 30 here
try:
    f2.participation = 500
    print(f2.participation)
except PercentageTooHighError:
    print('Exception PercentageTooHighError was raised')
try:
    f2.participation = -5
    print(f2.participation)
except PercentageTooLowError:
    print('Exception PercentageTooLowError was raised')
try:
    f2.participation = 'test'
    print(f2.participation)
except (TypeError, ValueError):
    print('Value is not a number')

