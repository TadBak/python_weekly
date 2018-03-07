def multiziperator(*args):
    generators = [(item for item in iterator) for iterator in args]
   
    while True:
        for gen in generators:
            yield next(gen)



