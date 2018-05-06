from numbers import Number

class Item:

    def __init__(self, quantity, measure, name, price_per_measure):
        if not isinstance(quantity, Number):
            raise TypeError
        else:
            self.quantity = quantity
        self.measure = measure
        self.name = name
        if not isinstance(price_per_measure, Number):
            raise TypeError
        else:
            self.price_per_measure = price_per_measure

    def get_short(self):
        return self.name


    def get_long(self):
        if int(self.quantity) == float(self.quantity):
            precision = 0
        else:
            precision = 2
        return (f'{self.quantity:{10}.{precision}f} {self.measure:{10}} ' 
                f'{self.name:{15}.{15}} @ ${self.price_per_measure:{5}.{2}f}' 
                f'...$ {self.quantity * self.price_per_measure:.{2}f}')


class Cart:

    def __init__(self):
        self.content = []

    def add(self, item):
        if not isinstance(item, Item):
            raise TypeError
        else:
            self.content.append(item)

    def __format__(self, spec):
        if spec == 'short':
            return ', '.join(item.get_short() for item in self.content)
        if spec == 'long':
            return '\n'.join(item.get_long() for item in self.content)



