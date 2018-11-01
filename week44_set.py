"""Populating the simple appointments database with the data supplied
by the user. Multiple appointment entries are possible. Before using this script
the database must be already created with the following schema:

CREATE TABLE Appointments (
               id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               comment TEXT,
               start_at TIMESTAMP NOT NULL,
               end_at TIMESTAMP NOT NULL )
"""

import sqlite3
import datetime
from collections import namedtuple

DATABASE = 'week44.db'
User_entry = namedtuple('User_entry', [
                'title',    # string - title is compulsory
                'comment',  # string - comment can be empty
                'start',    # datetime object - beginning of appointment
                'end'       # datetime object - end of appointment
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
            duration = datetime.timedelta(hours=hour, minutes=minute)
            if duration.total_seconds() > 0:
                break
            else:
                print('Please correct duration time')
        except ValueError:
            print('Please correct duration time')
    comment = input('Any comments? ')
    return User_entry(title, comment, start, start + duration)


# default mode is rwc, therefore non-existing database will be created,
# sucessfull transactions are commited automatically
with sqlite3.connect(DATABASE) as con:
    cur = con.cursor()
    # checking for the presence of Appointments table in connected database
    cur.execute('''PRAGMA table_info(Appointments)''')
    if len(cur.fetchall()) == 0:
        print(f'File {DATABASE} is not the expected database')
    else:
        # populating database with appointments
        while True:
            entry = get_user_input()
            cur.execute('''INSERT INTO Appointments (title, comment, start_at,
                        end_at) VALUES (?, ?, ?, ?)''', 
                        (entry.title, entry.comment, str(entry.start),
                         str(entry.end)))
            if input('Press Y to make next appointment: ').lower() != 'y':
                break
con.close()

