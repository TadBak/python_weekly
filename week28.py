import os
import time
from os.path import isdir
from flask import Flask, request
from week26 import FileInfo, FileList, DirectoryFileError
app = Flask(__name__)

PICKLE_STORE = '/tmp/'

@app.route('/scan/')    # both: /scan and /scan/ are accepted
def scan_dir():
    pathname = get_pathname()
    try:
        scan_data = FileList(pathname)
    except DirectoryFileError as e:
        return 'Directory does not exist or can not be read. ' + str(e)
    try:
        scan_data.store(file_name(scan_data.directory))
    except DirectoryFileError as e:
        return 'Data store error. ' + str(e)
    return (f'Directory: {scan_data.directory} scanned and gathered data saved.'
            f'<br/>Timestamp: {get_timestamp(scan_data)}')

@app.route('/rescan/')
def rescan_dir():
    pathname = os.path.abspath(get_pathname())
    if isdir(pathname) and os.access(pathname, os.R_OK):
        try:
            scan_data = FileList(file_name(pathname))
        except DirectoryFileError as e:
            return f'Directory {pathname} not scanned yet. ' + str(e)
    else:
        return f'Directory: {pathname} does not exist or can not be read.'
    diffs = scan_data.rescan()
    return (f'Changes in directory: {pathname} since {get_timestamp(scan_data)}' +
            '<br/>Added files:<br/>' + '<br/>'.join(diffs['added']) +
            '<br/>Deleted files:<br/>' + '<br/>'.join(diffs['removed']) +
            '<br/>Changed files:<br/>' + '<br/>'.join(diffs['changed']))

def get_pathname():
    pathname = request.query_string.decode('utf-8')
    if len(pathname) == 0:
        pathname = '.'
    return pathname

def file_name(name):
    return PICKLE_STORE + name.replace('/', '-')

def get_timestamp(scanned):
    return f'{time.strftime("%d %b %Y %H:%M:%S", time.localtime(scanned.timestamp))}'

if __name__ == '__main__':
    app.run(debug=True)

