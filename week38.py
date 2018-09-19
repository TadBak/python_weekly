import tarfile
import zipfile
from tempfile import TemporaryDirectory
import os.path as path

def convert_file(tar_name):
    """Converts one tar file of the name tar_name into zip file with the same
    basename. The function returns a string 'OK' on success or string describing
    conversion problem in case of a failure.
    """
    try:
        mytar = tarfile.open(tar_name)
    except (tarfile.ReadError, tarfile.CompressionError) as e:
        return f'Tar file {tar_name} opening error: {e}'
    zip_name = path.join(path.dirname(tar_name), 
                         path.basename(tar_name).split('.')[0] + '.zip')
    # the content of the tar file is extracted into temporary directory, which
    # is deleted automatically after zipping all files
    with TemporaryDirectory() as tmp:
        mytar.extractall(tmp)    
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
            for one_file in mytar.getnames():
                # supplying the arcname argument assures that leading paths of
                # the files will not be saved in the zip archive
                myzip.write(path.join(tmp, one_file), one_file)
            # comment is just for fun :-)
            myzip.comment = f'Converted from {tar_name}'.encode('utf-8')
            result = myzip.testzip()
            if result is not None:
                return f'File {result} in {zip_name} is corrupted'
    return 'OK'

def tar_to_zip(*names):
    """Converts batch of Unix .tar, .tar.gz, .tar.bz2 files into .zip files and
    saves them in the same directory as the original files. 
    """    
    print('Converting TAR files into ZIP files:')
    for name in names:
        print(f'\t{name} ... ', end='') 
        if path.exists(name):
            if tarfile.is_tarfile(name):
                print(convert_file(name))
            else:
                print('is not a TAR file!')
        else:
            print('does not exists or is inaccessible')
    print('All done.')
    
