from pathlib import Path
import hashlib

class DirFileHash:

    def __init__(self, dirname):
        self.path = Path(dirname)

    def __getitem__(self, key):
        if not self.path.joinpath(key).is_file():
            return None
        try:
            with open(self.path.joinpath(key), 'rb') as file_:
                return hashlib.md5(file_.read()).hexdigest()
        except PermissionError:
            return None


