import cmd

class Calculator(cmd.Cmd):

    intro = 'Simple calculator. For a list of available commands type: help\n'
    prompt = '<calculate>: '

    def get_positive_integers(self, line):
        """Extract positive integers from the input line.

        After processing the input string only positive integers are returned
        as a list of their string representation. Zero is also considered a
        positive integer, all other items are ignored. When the resulting list
        is empty (there were no positive integers in the input line) the method
        prints an empty line and returns None. When only one positive integer
        is found it is printed (as a number) and None is returned.

        Parameters
        ----------
        line : str
            Input string containing several items separated by spaces.

        Returns
        -------
        list of strings or None
            List of string representations of positive integer numbers.
        """

        arguments = [arg for arg in line.split() if arg.isdigit()]
        if len(arguments) > 1:
            return arguments
        print(int(arguments[0])) if len(arguments) == 1 else print()
        return None

    def operate(self, line, operator):
        """Perform mathematical operation and print the result.

        Parameters
        ----------
        line : str
            Input string containing several items separated by spaces.
        operator : str
            One of the mathematical operators applied to numerical arguments,
            it can be: +, -, *, or //

        Returns
        -------
        None
        """

        data = self.get_positive_integers(line)
        if data is not None:
            # at least two positive integers are available
            print(eval(operator.join(data)))

    def precmd(self, line):
        """Alter command line before its processing.

        When arithmetic operators are used instead of commands in the input
        line, they are replaced with the corresponding commands first.

        Parameters
        ----------
        line : str
            Input string containing several items separated by spaces.

        Returns
        -------
        string
            Either the original input string or the string with symbol operators
            replaced with commands.
        """

        ops = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div'}
        items = line.split()
        if items[0] in ops:
            items[0] = ops[items[0]]
            return ' '.join(items)
        else:
            return line

    def do_add(self, line):
        self.operate(line, '+')

    def help_add(self):
        print('Add together two or more positive integer numbers. All other\n'
              'arguments will be ignored.')

    def do_sub(self, line):
        self.operate(line, '-')

    def help_sub(self):
        print('Subtract two or more positive integer numbers taking arguments\n'
              'from left to right. All other arguments will be ignored.')

    def do_mul(self, line):
        self.operate(line, '*')

    def help_mul(self):
        print('Multiply two or more positive integer numbers taking arguments\n'
              'from left to right. All other arguments will be ignored.')

    def do_div(self, line):
        try:
            self.operate(line, '//')
        except ZeroDivisionError:
            print('Can not divide by zero')

    def help_div(self):
        print('Perform integer division of two or more positive integer numbers\n'
              'taking arguments from left to right. All other arguments will\n'
              'be ignored.')

    def do_EOF(self, line):
        """Press Ctrl-D to finish working with the calculator."""
        return True

    def do_quit(self, line):
        """Alternative way to finish working with the calculator."""
        return True

    def postloop(self):
        print('Bye!')


if __name__ == '__main__':
    Calculator().cmdloop()

