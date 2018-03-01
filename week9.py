import random
from itertools import chain
import re
import operator

MAXNUMBER = 40                          # largest number used in exercises
LINES = 100                             # number of exercises in a file
FILENAME = 'math_exercise.txt'          # name of file with exercises
random.seed()


def write_line(maxn):
    """ Randomly generate one exercise line
        Arguments:
            maxn - largest number used to generate exercise (integer)
        Returns:
            string with one exercise
    """
    width = len(str(maxn)) + 1
    line = ([f'{random.randint(-maxn,maxn):{width}}'] +
            list(
                 chain.from_iterable((random.choice('+-'), 
                                      f'({random.randint(-maxn,maxn):{width}})')
                                     for _ in range(3))) +
            ['= ____'])
    return ' '.join(line)


def write_file(file_, maxn, maxl):
    """ Write exercises to a file
        Arguments:
            file_ - the name of the file to write (string)
            maxn - largest number used to generate exercises (integer)
            maxl - number of exercises in a file (integer)
        Returns:
            nothing
    """
    width = len(str(maxl))
    with open(file_, 'w') as out:
        for i in range(1, maxl+1):
            out.write(f'[{i:{width}}] ' + write_line(maxn) + '\n')
 

def process_line(line):
    """ Calculate the result of one exercise
        Arguments:
            line - one exercise (string)
        Returns:
            total - the result of calculations (integer)
    """
    action = {'+': operator.add, '-': operator.sub}
    nums = [int(num) for num in re.findall(r'-?\d+', line)[1:]] # extracts numbers
    ops = re.findall(r' ([+-]) ', line)                         # extracts operators
    total = nums[0]
    for op, num in zip(ops, nums[1:]):
        total = action[op](total, num)
    return total


def print_solutions(file_):
    """ Print solutions of exercises from the file
        Arguments:
            file_ - the name of the file to read (string)
        Returns:
            nothing
    """
    with open(file_, 'r') as inp:
        for line in inp:
            print(line[:-5] + str(process_line(line)))


if __name__ == '__main__':
    write_file(FILENAME, MAXNUMBER, LINES)
    print_solutions(FILENAME)

