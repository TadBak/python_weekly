import sys

class Tee:
    """ Simple class for writing text data into several file-like objects.
        None of the raised exceptions is caught in this class but passed to
        the caller.
    """

    def __init__(self, *args):
        self.outs = args

    def write(self, str):
        for fileobj in self.outs:
            fileobj.write(str)

    def writelines(self, str):
        self.write(str + '\n')

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        for fileobj in self.outs:
            if fileobj is sys.stdout:
                fileobj.flush()
            else:
                fileobj.close()


