def multiziperator(*args):
    """ Returns interleaved elements from all input iterators until the shortest
        one is exhausted, consequently the number of returned elements coming
        from different iterators can not be the same.
    """
    generators = [(item for item in iterator) for iterator in args]
    while True:
        for gen in generators:
            yield next(gen)


def multiziperator(*args):
    """ Returns interleaved elements from all input iterators in such a way that
        the number of returned elements coming from different iterators is the 
        same and equal to the length of the shortest iterator.
    """
    shortest = min([len(iterator) for iterator in args])
    generators = [(item for item in iterator) for iterator in args]
    for _ in range(shortest):
        for gen in generators:
            yield next(gen)

