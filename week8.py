import os
from pathlib import Path
import pprint


class DirNotAccessible(Exception):
    pass


class FileTooSmall(Exception):
    pass


def file_length(filename):
    return os.stat(filename).st_size


def big_file(filename):
    size = os.stat(filename).st_size
    if size < 10000:
        raise FileTooSmall('File smaller than 10000 bytes')
    return size


def filefunc(directory, custom_func):
    """ Function applies custom function to all regular files in the directory.
        Arguments:
            directory - name of the directory (string)
            custom_func - name of the function which takes as an argument the
                name of the file
        Returns:
            success - dictionary, where key is the file name and value is the
                output of custom function after successful run
            failure - dictionary, where key is the file name and value is the
                Exception object thrown by custom function
        Function raises DirNotAccessible exception if directory does not
        exists or can not be accessed due to permission issues
    """
    work_dir = Path(directory)
    if os.access(work_dir, os.F_OK | os.R_OK) and work_dir.is_dir():
        success = {}
        failure = {}
        for file_ in work_dir.iterdir():
            if file_.is_file():
                try:
                    success[file_.name] = custom_func(file_.resolve())
                except Exception as e:
                    failure[file_.name] = e
        return success, failure
    else:
        raise DirNotAccessible(
                f'Directory {directory} does not exist or is not accessible')


if __name__ == '__main__':
    success_dir, failure_dir = filefunc('/etc', big_file)
    pp = pprint.PrettyPrinter()
    print('--- Success dictionary ---')
    pp.pprint(success_dir)
    print('--- Failure dictionary ---')
    pp.pprint(failure_dir)

