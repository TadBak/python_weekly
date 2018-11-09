"""Script processes MP4 files in the given directory and prints some
statistics information related to these files.
"""

import glob
from tinytag import TinyTag
import os
import pandas as pd
import sys


def acquire_data(dirname):
    """Scans the directory dirname for files with .mp4 extension.

    The return value has two components: the first one is a list of 2-element
    tuples, where the first element is the name of the file and the second is
    TinyTag object associated with that file. The second component of the 
    returned value is the name (potentially modified) of the processed
    directory. If that directory does not exist function returns None. 
    """

    if not os.path.isdir(dirname):
        return None
    dirname = dirname.rstrip('/')   # just in case
    mp4s = [(os.path.basename(pathname), TinyTag.get(pathname)) for pathname
            in glob.iglob(dirname + '/*.mp4')]
    return mp4s, dirname


def prepare_data(mp4_files, ds_name=None):
    """Prepare the acquired data for further analysis.

    Function takes a list prepared by acquire_data, then extracts the duration
    of each MP4 video and combines them into a pandas series. Optionally, the
    name of this series can be set as well.
    """

    # idiom to 'transpose' the list, see:
    # stackoverflow.com/questions/40850764/quickest-way-to-to-convert-list-of-tuples-to-a-series
    data = list(zip(*[(item[0], item[1].duration) for item in mp4_files]))
    series = pd.Series(data[1], index=data[0])/60   # durations in minutes now
    # tinytag processes all files with .mp4 extension, even if the file is not
    # a MP4 video - in such a case the duration is None 
    series.dropna(inplace=True)
    if ds_name:
        series.name = ds_name
    return series


def print_report(series):
    """Prints statistics information related to MP4 files."""

    print(f'Statistics of MP4 files in directory: {series.name}')
    print(f'\tNumber of MP4 videos: {len(series)}')
    m, s = divmod(series.sum()*60, 60)
    print(f'\tTotal playing time: {int(m):d}:{int(round(s)):02d}')
    print(f'\tShortest video: {series.min():.3f} minutes ({series.idxmin()})')
    print(f'\tLongest video: {series.max():.3f} minutes ({series.idxmax()})')
    print(f'\tMean playing time: {series.mean():.3f} minutes')
    print(f'\tStandard deviation: {series.std():.3f} minutes')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Script expect one argument -- the name of a directory to process')
        sys.exit()
    info = acquire_data(sys.argv[1])
    if info is None:
        print(f'Directory {sys.argv[1]} does not exist')
        sys.exit()
    if not info[0]:
        print('There are no MP4 files in the specified directory')
        sys.exit()
    ds = prepare_data(*info)
    if len(ds) == 0:
        print('There are only faked MP4 file(s) in the specified directory')
        sys.exit()
    print_report(ds)

