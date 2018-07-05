import os
from flask import Flask
app = Flask(__name__)

@app.route('/scan/')
@app.route('/scan/<path:directory>')
def show_files(directory=None):
    if directory is None:
        return 'Please provide the name of a directory to scan'
    absolute_dir = '/' + directory
    if os.path.isdir(absolute_dir):
        if os.access(absolute_dir, os.R_OK):
            return list_directory(absolute_dir)
        else:
            return f'No permission to read: {absolute_dir}'
    else:
        return f'Directory: {absolute_dir} does not exists'

def list_directory(path):
    files_list = []
    for root, dirs, files in os.walk(path):
        files_list.append(root)
        for one_file in files:
            files_list.append(f'{os.path.join(root, one_file)}')
    return '<br/>'.join(files_list)


if __name__ == '__main__':
    app.run(debug=True)

