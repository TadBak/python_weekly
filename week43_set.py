"""Populating the simple appointments database with the data supplied
by the user. Multiple appointment entries are possible.
"""

import sqlite3
from contextlib import closing
import datetime
from collections import namedtuple

DATABASE = 'week43.db'
User_entry = namedtuple('User_entry', [
                'title',    # title is compulsory
                'comment',  # comment can be empty
                'start',    # string representation of datetime object
                'hours',    # integer, hours of appointment duration
                'minutes'   # integer, minutes in addition to hours duration
             ])


def get_user_input():
    """Returns validated user input for inclusion into a database."""

    print('--- New appointment entry ---')
    while True:
        title = input("Appointment's title? ")
        if len(title) == 0:
            print('Title can not be empty')
        else:
            break
    while True:
        print('Date and time of the appointment:')
        day = input('\tDay? ')
        month = input('\tMonth (number)? ')
        year = input('\tYear? ')
        hour = input('\tHour (24h clock)? ')
        minute = input('\tMinute? ')
        # successful conversion into datetime object indicates correct values
        # entered by user
        try:
            start = datetime.datetime(int(year), int(month), int(day), 
                                  int(hour), int(minute))
            break
        except ValueError:
            print('Please correct date and time')
    while True:
        print('Duration of the appointment:')
        # hour and minute of appointment duration must be non-negative integers,
        # total duration can not be zero
        try:
            hour = int(input('\tHours? '))
            minute = int(input('\tMinutes? '))
            if hour >= 0 and minute >= 0 and hour + minute > 0:
                break
            else:
                print('Please correct duration time')
        except ValueError:
            print('Please correct duration time')
    comment = input('Any comments? ')
    return User_entry(title, comment, str(start), hour, minute)


# context manager assures that database connection is closed automatically
with closing(sqlite3.connect(DATABASE)) as con:
    # sucessfull transactions are commited automatically
    with con:
        cur = con.cursor()
        # appointments start and end timestamps are stored as UTC julian dates,
        # therefore independent of time zones and daylight savings
        cur.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    title TEXT NOT NULL,
                    comment TEXT,
                    start REAL,
                    end REAL)''')
        while True:
            entry = get_user_input()
            # the end timestamp is calculated during insertion using SQLite
            # date and time function
            cur.execute('''INSERT INTO appointments VALUES (
                        ?, ?, julianday(?, 'utc'), julianday(?, ?, ?, 'utc'))''', 
                        (entry.title, entry.comment, entry.start, entry.start, 
                        f'+{entry.hours} hour', f'+{entry.minutes} minute'))
            if input('Press Y to make next appointment: ').lower() != 'y':
                break
   
