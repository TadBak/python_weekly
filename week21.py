def mygetter(*args):

    def get_items(iterable):
        if len(args) == 1:
            return iterable[args[0]]
        else:
            return tuple(iterable[arg] for arg in args)

    return get_items
        
