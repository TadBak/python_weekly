from collections import namedtuple
from collections import Counter
import sys
from itertools import groupby


Person = namedtuple('Person', 'first, last')


class TableFull(Exception):
    def __init__(self, table_num, max_seats):
        self.msg = (f'Table {str(table_num)} is already at full capacity of '
               f'{str(max_seats)} persons')
        super(TableFull, self).__init__(self.msg)
        self.table_num = table_num
        self.max_seats = max_seats


class GuestList(object):
    """Simple weeding guests organiser.
    """
    _MAX_SEATS = 10         # maximum number of seats at each table

    def __init__(self):
        self._guests = {}   # keys in this dictionary will be Person objects,
                            # as it is assumed that all names are unique

    def assign(self, person, table=None):
        """ Adding guests or changing their sitting arrangements.
            Arguments:
                person - an instance of named tuple Person
                table - table numer (integer), can be ommitted
            This method can raise TableFull exception 
        """
        if not table is None:
            if len([table_num for person, table_num in self._guests.items()
                   if table_num == table]) >= GuestList._MAX_SEATS:
                raise TableFull(table, GuestList._MAX_SEATS)
        self._guests[person] = table

    def __len__(self):
        return len(self._guests)

    def table(self, number):
        """ List of guests at given table.
            Arguments:
                number - table number (integer)
        """
        return [person for person, table_num in self._guests.items()
                if table_num == number]

    def unassigned(self):
        """ List of guests not assigned to any table.
        """
        return [person for person, table_num in self._guests.items()
                if table_num is None]  

    def free_space(self):
        """ Dictionary of free spaces at already occupied tables, number of
            the table is the key.
        """
        return {table_num: GuestList._MAX_SEATS - occupied 
                for (table_num, occupied) 
                in Counter(self._guests.values()).items()
                if table_num is not None}

    def _sort_guests(self):
        """ Internal generator for sorting guests by table number, last name
            and first name. Unallocated guests are at the end, sorted by last
            name and first name.
        """
        return (item for item in sorted(self._guests.items(), 
                key = lambda t: (t[1], t[0].last, t[0].first)
                      if t[1] is not None
                      else (sys.maxsize, t[0].last, t[0].first)))

    def guests(self):
        """ Sorted list of all guests.
        """
        return [' '.join(person) for person, _ in self._sort_guests()]

    def __repr__(self):
        """ Formatted sorted list of all guests, ready for printing.
        """
        lines = []
        for key, group in groupby(self._sort_guests(), key = lambda t: t[1]):
            lines.append(str(key))
            for person in list(group):
                lines.append('\t' + person[0].last + ', ' + person[0].first)
        return '\n'.join(lines)

"""
    def __repr__(self):
        lines = ([str(key) + '\n'] + ['\t' + person[0].last + ', ' +
                  person[0].first + '\n' for person in list(group)]
                  for key, group in groupby(self._sort_guests(),
                      key = lambda t: t[1]))
        return ''.join(item for table in lines for item in table)
"""


if __name__ == '__main__':
    gl = GuestList()
    gl.assign(Person('Waylon', 'Dalton'), 1)
    gl.assign(Person('Justine', 'Henderson'), 1)
    gl.assign(Person('Abdullah', 'Lang'), 3)
    gl.assign(Person('Marcus', 'Cruz'), 1)
    gl.assign(Person('Thalia', 'Cobb'), 2)
    gl.assign(Person('Mathias', 'Little'), 2)
    gl.assign(Person('Eddie', 'Randolph'), None)
    gl.assign(Person('Angela', 'Walker'), 2)
    gl.assign(Person('Lia', 'Shelton'), 3)
    gl.assign(Person('Hadassah', 'Hartman'), None)
    gl.assign(Person('Joanna', 'Shaffer'), 3)
    gl.assign(Person('Jonathon', 'Sheppard'), 2)

    print(f'--- Total number of guests:\n\t{len(gl)}')
    print(f'--- Guests at table 3:\n\t{gl.table(3)}')
    print(f'--- Guests not assigned to any table:\n\t{gl.unassigned()}')
    print('--- Changing assignation...')
    p = Person('Joanna', 'Shaffer')
    gl.assign(p, 2)
    print(f'--- Guests at table 3:\n\t{gl.table(3)}')
    print(f'--- Guests at table 2:\n\t{gl.table(2)}')
    print(f'--- Free space at each table:\n\t{gl.free_space()}')
    print(f'--- List, sorted by table, last and first name of all guests:'
          f'\n\t{gl.guests()}')
    print(f'--- Formatted list of all guests:')
    print(gl)
    print('--- Filling table 5 to capacity...')
    for i in range(10):
        gl.assign(Person('First' + str(i), 'Last' + str(i)), 5)
    print(f'--- Free space and guests at table 5:\n\t{gl.free_space()}'
          f'\n\t{gl.table(5)}')
    print('--- Overflowing table 5...')
    try:
        gl.assign(Person('John', 'Doe'), 5)
    except TableFull as e:
        print(e.msg)







