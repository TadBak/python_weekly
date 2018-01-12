def _get_arguments(*args):
    """Helper function which prepares input data for custom myrange2 and
    myrange3 functions. It makes sure that at least one but no more than three
    integers were supplied. Returns tuple of three integers, where the last 
    number is never zero. Can raise TypeError or ValueError exceptions in case
    of wrong input data.
    """

    def no_arguments():
        raise TypeError('range expected at least 1 arguments, got 0')

    def one_argument():
        return 0, args[0], 1

    def two_arguments():
        return args[0], args[1], 1

    def three_arguments():
        return args[0], args[1], args[2]

    selector = {
        0: no_arguments,
        1: one_argument,
        2: two_arguments,
        3: three_arguments }
  
    try:
        arguments = selector[len(args)]()
    except KeyError:
        raise TypeError(
                'range expected at most 3 arguments, got {}'.format(
                len(args))) from None

    for item, position in zip(arguments, ('start', 'end', 'step')):
        if not isinstance(item, int):
            raise TypeError(
                    'range() integer {} argument expected'.format(position))

    if arguments[2] == 0:
        raise ValueError('range() step argument must not be zero')

    return arguments


def myrange2(*args):
    """Custom range function, returns list.
    """
    start, stop, step = _get_arguments(*args)
    out = []
    condition = {
        '+': lambda: start < stop,
        '-': lambda: start > stop }
    flag = '+' if step > 0 else '-'
    while condition[flag]():
        out.append(start)
        start += step
    return out


def myrange3(*args):
    """Custom range function, returns generator.
    """
    start, stop, step = _get_arguments(*args)
    condition = {
        '+': lambda: start < stop,
        '-': lambda: start > stop }
    flag = '+' if step > 0 else '-'
    while condition[flag]():
        yield start
        start += step




