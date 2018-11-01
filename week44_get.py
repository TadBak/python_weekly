"""Retrieving all entries from the simple appointments database and presenting
them to the user. Additionally, for selected countries a check is performed
whether there is a collision with national holidays.
"""

import sqlite3
from contextlib import closing
import datetime
import holidays

DATABASE = 'week44.db'
# clients' countries
COUNTRIES = ['US', 'AU', 'UK']
client_holidays = {country: holidays.CountryHoliday(country) for country in COUNTRIES}

# context manager assures that database connection is closed automatically
with closing(sqlite3.connect(DATABASE)) as con:
    con.row_factory = sqlite3.Row
    # sucessfull transactions are commited automatically
    with con:
        cur = con.cursor()
        cur.execute('''SELECT start_at as start, end_at as stop, title 
                    FROM Appointments ORDER BY start_at''')
        entries = cur.fetchall()

print('Scheduled appointments:\n-----')
if entries:
    for entry in entries:
        start = datetime.datetime.strptime(entry['start'], '%Y-%m-%d %H:%M:%S')
        stop = datetime.datetime.strptime(entry['stop'], '%Y-%m-%d %H:%M:%S')
        print(f"{start.strftime('%b %d, %Y, %H:%M-')}{stop.strftime('%H:%M.')} "
              f"{entry['title']} ", end='')
        for country in client_holidays:
            if start.date() in client_holidays[country]:
                print(f'{country} holiday: {client_holidays[country].get(start.date())} ',
                      end='')
        print()
else:
    print('No appointments!')



