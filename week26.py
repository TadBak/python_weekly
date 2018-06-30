import os
from os.path import join, isfile, isdir
import hashlib
import time
import pickle


class FileInfo:
    """ Generates and stores information about a single file on disk: its
        absolute path, time of the last modification and SHA-1 digest of its
        content.
    """
    def __init__(self, filepath):
        # storing an absolute path of the file assures that every one is unique
        self.filepath = os.path.abspath(filepath)
        self.timestamp = os.stat(self.filepath).st_mtime
        self.sha1 = self.get_sha1(self.filepath)

    @staticmethod   # can be used as a class method
    def get_sha1(file_name):
        """ Returns an SHA-1 digest of the file given by its name: file_name. 
            Returns None if the file could not be read. The method processes
            file contents in chunks of BUFSIZE size, threfeore it is suitable
            for large files as well.
        """
        BUFSIZE = 1048576   # 1MB chunk, can be optimised if needed
        sha1 = hashlib.sha1()
        try:
            with open(file_name, 'rb') as f:
                while True:
                    data = f.read(BUFSIZE)
                    if not data:
                        break
                    sha1.update(data)
            return sha1.hexdigest()
        except IOError:
            return None

    def __eq__(self, other):
        """ Defines equivalenece of objects by comparing all its attributes."""
        return vars(self) == vars(other)

    def __hash__(self):
        """ All absolute paths are unique, therefore it is sufficient to
            calculate hash of the filepath only.
        """
        return hash(self.filepath)

    def __str__(self):
        """ Helps to print the values of the object attributes."""
        return (f'filepath:\t{self.filepath}\n'
                f'timestamp:\t{self.timestamp}\n'
                f'sha1:\t\t{self.sha1}')


class DirectoryFileError(Exception):
    """ Custom exception class used by FileList objects."""
    pass


class FileList:
    """ Generates and stores information about files in the given directory.
        The DirectoryFileError custom exception is raised if directories or
        files can not be accessed.
    """

    def __init__(self, arg=None):
        """ When the FileList object is instantiated without any arguments then
            the current directory is processed. When the name of the directory
            is given then that directory and its subdirectories are processed.
            Alternatively, when the argument is the name of the file, then it is
            assumed that file contains serialised attributes of FileList object
            and an attempt is made to restore the object.
        """
        if arg is None:
            path = os.path.abspath('.')
        else:
            path = os.path.abspath(arg)
        if isdir(path) and os.access(path, os.R_OK):
            self.files_info = self._get_files_info(path)    # set of FileInfo objects
            self.timestamp = time.time()                    # current time
            self.directory = path                           # absolute directory
        elif isfile(path) and os.access(path, os.R_OK):
            self._load_data(path)                           
        else:
            raise DirectoryFileError(f'Unable to process: {path}')
 
    def _get_files_info(self, directory):
        """ Returns the set of FileInfo objects, each object for one file within
            directory and its subdirectories.
        """
        files_info = set()
        for root, dirs, files in os.walk(directory):
            for one_file in files:
                one_file_path = join(root, one_file)
                if isfile(one_file_path):   # include only regular files
                    files_info.add(FileInfo(one_file_path))
        return files_info

    def rescan(self):
        """ Scans again the same directory and finds the differences since the
            previous scan. Returns a dictionary with the keys: added - list of
            added files, removed - list of removed files, changed - list of
            changed files (altered SHA-1 digest).
        """
        new_info = self._get_files_info(self.directory)
        # updates is a set of FileInfo objects which are not common to both,
        # files_info and new_info sets, i.e. updates set represents all added,
        # removed and changed files
        updates = self.files_info.symmetric_difference(new_info)
        added = {item for item in updates if item.filepath not in
                    {item.filepath for item in self.files_info}}
        removed = {item for item in updates if item.filepath not in
                    {item.filepath for item in new_info}}
        changed = updates.difference(added).difference(removed)
        report = {}
        report['added'] = [item.filepath for item in added]
        report['removed'] = [item.filepath for item in removed]
        # each modified file is represented by two FileInfo objects in the
        # changed set, but generating a set of their names removes duplicates
        report['changed'] = list({item.filepath for item in changed})
        self.files_info = new_info
        self.timestamp = time.time()
        return report

    def default_file_name(self):
        """ Generates a default file name for storing serialised attributes of
            FileList object. The name is composed of the base name of the
            scanned directory and the date and time of the last scan. Such file
            is saved in the /tmp directory.
        """
        return (f'/tmp/{os.path.basename(self.directory)}_'     
                f'{time.strftime("%d%b%Y_%H%M%S", time.localtime(self.timestamp))}')

    def store(self, out_file=None):
        """ Stores on disk in the file out_file the serialised attributes of
            the current FileList object. Raises DirectoryFileError exception
            if the operation failed.
        """
        if out_file is None:
            out_file = self.default_file_name()
        try:
            with open(out_file, 'wb') as outfile:
                pickle.dump(vars(self), outfile, protocol=pickle.HIGHEST_PROTOCOL)
        except (IOError, pickle.PicklingError):
            raise DirectoryFileError(f'Unable to save: {out_file}')

    def _load_data(self, in_file):
        """ Restores from the in_file previously saved attributes of the
            FileList object. Raises DirectoryFileError if the operation was
            not successful.
        """
        try:
            with open(in_file, 'rb') as infile:
                self.__dict__ = pickle.load(infile)
        except (IOError, AttributeError, pickle.UnpicklingError):
            raise DirectoryFileError(f'Unable to load: {in_file}')

