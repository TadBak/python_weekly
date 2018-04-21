from numbers import Number

class TresholdEqual:
    """ Implementation of numeric objects considered equal when within a
        specified tolerance. The optional 'tolerance' parameter defaults to 1.
        Only comparison operators are implemented. Attempt to compare with
        objects of different types raises TypeError exception. When two
        TresholdEqual objects have different tolerances the smaller one takes
        precendence.
    """

    def __init__(self, number, tolerance=1):
        if not isinstance(number, Number):
            raise TypeError
        else:
            self.number = number
        if not isinstance(tolerance, Number):
            raise TypeError
        else:
            self.tolerance = tolerance

    def __eq__(self, other):
        if isinstance(other, type(self)):
            tolerance = min(self.tolerance, other.tolerance)
            return abs(self.number - other.number) <= tolerance
        else:
            raise TypeError

    def __ne__(self, other):
        return not self == other


    def __lt__(self, other):
        return self != other and self.number < other.number

    def __gt__(self, other):
        return self != other and self.number > other.number

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other





