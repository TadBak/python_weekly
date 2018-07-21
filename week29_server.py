""" Simple directories monitoring server.

This server listens on port 5000 of the localhost and responds to the following
URL commands:
    http://127.0.0.1:5000/scan/?<directory_name>
    http://127.0.0.1:5000/rescan/?<directory_name>
where <directory_name> is the name of the directory to monitor. The first 
command takes a snaphot of a given directory, while the second compares the
directory with the previosuly taken snapshot and reports all added, removed and
changed files. The server sends back the JSON responses using the following 
format:
{
    "data": {
                "added": [ ... ],
                "changed": [ ... ],
                "removed": [ ... ]
            },
    "message": " ... ",
    "pathname": " ... ",
    "status" : number,
    "timestamp": " ... "
}
Only "message", "pathaname" and "status" are always present, the status number
indicates whether the command was completed successfuly (status 0) or an error
has occured (status < 0). The message string contains the description of the
response, the pathname string the name of the processed directory. The "data"
object, if present, is composed of 3 arrays: "added", "changed" and "removed",
each of them lists the names of added, changed or deleted files. The "timestamp"
strings shows the date and time when the directory was last scanned, it is 
present only when the status is 0.
"""
import os
import time
from os.path import isdir
from flask import Flask, request, jsonify
from week26 import FileInfo, FileList, DirectoryFileError

PICKLE_STORE = '/tmp/'
app = Flask(__name__)

@app.route('/scan/')    # both: /scan and /scan/ are accepted
def scan_dir():
    pathname = get_pathname()
    try:
        scan_data = FileList(pathname)
    except DirectoryFileError as e:
        return get_json(-1, pathname, 
                f'Directory does not exist or can not be read. {str(e)}')
    try:
        out_file = file_name(scan_data.directory)
        scan_data.store(out_file)
    except DirectoryFileError as e:
        return get_json(-3, out_file, f'Data store error. {str(e)}')
    return get_json(0, scan_data.directory,
                'Directory scanned and gathered data saved.',
                get_timestamp(scan_data))

@app.route('/rescan/')
def rescan_dir():
    pathname = os.path.abspath(get_pathname())
    if isdir(pathname) and os.access(pathname, os.R_OK):
        try:
            scan_data = FileList(file_name(pathname))
        except DirectoryFileError as e:
            return get_json(-2, pathname, f'Directory not scanned yet. {str(e)}')
    else:
        return get_json(-1, pathname, 
                f'Directory: {pathname} does not exist or can not be read.')
    diffs = scan_data.rescan()
    return get_json(0, pathname, 'Changes in directory since last scan',
            get_timestamp(scan_data), diffs)

def get_pathname():
    pathname = request.query_string.decode('utf-8')
    if len(pathname) == 0:
        pathname = '.'
    return pathname

def file_name(name):
    return PICKLE_STORE + name.replace('/', '-')

def get_timestamp(scanned):
    return f'{time.strftime("%d %b %Y %H:%M:%S", time.localtime(scanned.timestamp))}'

def get_json(status, pathname, message, timestamp=None, data=None):
    response = {}
    response['status'] = status
    response['pathname'] = pathname
    response['message'] = message
    if timestamp is not None:
        response['timestamp'] = timestamp
    if data is not None:
        response['data'] = data
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

