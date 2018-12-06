from enum import Enum
import random


class OrderedEnum(Enum):
    """Ordered enumeration subclass.

    By implementing comparison operators the objects of this class can be
    compared to each other, based on their values. For sorting purposes only
    __lt__ method need to be implemented. This code was copied from Python
    documentation: https://docs.python.org/3.6/library/enum.html#orderedenum 
    """

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class CardSuit(OrderedEnum):
    """Playing cards suits."""

    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

    def __str__(self):
        """User-friendly string representation of card's suit.

        UTF-8 has code points for characters representing suits, this string
        representation takes advantage of this fact.
        """

        char = {CardSuit.CLUBS.name: '\u2663', CardSuit.DIAMONDS.name: '\u2666', 
                CardSuit.HEARTS.name: '\u2665', CardSuit.SPADES.name: '\u2660'}
        return f'{char[self.name]}'

    # alternative method implementing Reuven's specifications
    #def __str__(self):
    #    return f'{self.name}'


class CardValue(OrderedEnum):
    """Playing cards values."""

    A = 1           # ace
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    J = 11          # jack
    Q = 12          # queen
    K = 13          # king

    def __str__(self):
        """User-friendly string representation of card's value.

        Numbers are represented as numbers, other values as single letters.
        """

        if self.value > 1 and self.value < 11:
            return f'{self.value}'
        else:
            return f'{self.name}'

    # alternative method implementing Reuven's specifications
    #def __str__(self):
    #    return f'{self.value}'


class Card:
    """Representation of a single card.

    Arguments
    ---------
    suit : CardSuit
        Suit of the card.
    value : CardValue
        Value of the card.
    """

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return repr(self.suit) + repr(self.value)

    def __str__(self):
        """User-fiendly string representation of the card."""

        return f'{self.suit}{self.value}'

    # alternative method implementing Reuven's specifications
    #def __str__(self):
    #    return f'{self.value} of {self.suit}'


if __name__ == '__main__':
    deck = [Card(s, v) for s in CardSuit for v in CardValue]
    hand = [str(card) for card in sorted(
                [deck[idx] for idx in random.sample(range(len(deck)), 5)],
                    key = lambda Card: (Card.suit, Card.value))]
    print(hand)

