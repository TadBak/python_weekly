import os

class TempFile:
    """Automatically erased temporary file.
    
    Given the pathname create a write-only file object which can be
    used inside a contex manager. When the object is garbage collected
    the underlying file is deleted from the disk. This object can raise
    the same exceptions as the regular file object.
    """

    def __init__(self, pathname, mode='w', *args):
        self.file = open(pathname, mode, *args)
        self.pathname = pathname
        
    def write(self, data):
        self.file.write(data)
        
    def close(self):
        self.file.close()
        
    def __del__(self):
        # exceptions raised within this method are ignored
        os.remove(self.pathname)
           
    def __enter__(self):
        return self.file
        
    def __exit__(self, *args):
        self.file.close()
        
            
