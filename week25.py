import os
from os.path import join, isfile
import hashlib
import sys
import pprint


def get_hash(file_name):
    BUFSIZE = 1048576   # 1MB chunk
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


def sha_info(directory):
    return [{'file': join(root, one_file),
             'timestamp': int(os.stat(join(root, one_file)).st_mtime),
             'sha1': get_hash(join(root, one_file))}
                for root, dirs, files in os.walk(directory)
                for one_file in files if isfile(join(root, one_file))]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Name of the directory expected, found none')
    elif not os.access(sys.argv[1], os.R_OK):
        print(f'Unable to process {sys.argv[1]} directory')
    else:
        pprint.pprint(sha_info(sys.argv[1]))

