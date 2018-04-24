def magic_tuples(sum, max):
    for x in range(sum - max + 1, max):
        yield sum - x, x

