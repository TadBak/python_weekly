"""Retrieving from the simple appointments database all entries for the current
day and presenting them to the user.
"""

import sqlite3
from contextlib import closing
import datetime

DATABASE = 'week43.db'

# context manager assures that database connection is closed automatically
with closing(sqlite3.connect(DATABASE)) as con:
    # sucessfull transactions are commited automatically
    with con:
        cur = con.cursor()
        now = str(datetime.date.today())
        print(f'Appointments for today: {now}\n-----')
        cur.execute('''SELECT time(start, 'localtime'), time(end, 'localtime'),
                       title, comment FROM appointments 
                       WHERE date(start, 'localtime') = ? 
                       ORDER BY time(start, 'localtime')''', (now, ))
        entries = cur.fetchall()
        if entries:
            for entry in entries:
                print(f'From {entry[0][:-3]} to {entry[1][:-3]} -> {entry[2]}')
                print(f'\t{entry[3]}\n')
        else:
            print('No appointments!')


