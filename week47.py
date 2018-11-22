from collections import namedtuple
import datetime as dt


class MeetingRoomTakenException(Exception):
    """Raised when double booking occurs."""
    pass


class MeetingNotFound(Exception):
    """Raised when particular meeting is not found."""
    pass


class MeetingRoom:
    """Scheduling and keeping track of meetings in a single room.

    Public methods
    --------------
    add_meeting(name, date_time, duration)
        Adds meeting to the schedule if there is no conflicting overlap.
    cancel_meeting(date_time)
        Cancels scheduled meeting identified by its date and time.
    daily_meetings(date)
        Lists all meetings in the room at a given date.
    purge_past_meetings()
        Removes all old meetings, scheduled for days before the current day.
    """

    # container for storing information about the meeting: its name (string)
    # and duration (timedelta object)
    MeetingInfo = namedtuple('MeetingInfo', 'name duration')

    def __init__(self, room):
        """Initialisation of MeetingRoom objects."""

        # meeting room identification
        self.room = room
        # collection of all meetings in the room; the keys in the dictionary
        # are datetime objects (meeting's date and time), the values are
        # MeetingInfo named tuples, which provide additional information about
        # the meetings 
        self.meetings = {}
 
    def __str__(self):
        """User friendly representation of a MeetingRoom object."""

        out = [f'Object {self.__class__.__name__}\n']
        for k, v in vars(self).items():
            out.append(f'\t{k}: {v}\n')
        return ''.join(out)

    def _is_overlap(self, start1, end1, start2, end2):
        """Test for overlap of two ranges.

        The detailed explanation of this trick can be found at:
        https://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html

        Parameters
        ----------
        start1, end1, start2, end2 : obj
            Beginnings and ends of ranges 1 and 2, respectively. These objects
            must implement the __gt__ method.

        Returns
        -------
        True or False
            Indication whether ranges overlap or not.            
        """

        return end1 > start2 and end2 > start1

    def add_meeting(self, name, date_time, duration):
        """Adds one meeting to the room booking.

        The new meeting is added to the room booking only if there is no overlap
        with the already existing meeting.

        Parameters
        ----------
        name : str
            The title (name) of the meeting.
        date_time : str
            Date of the meeting and the time when it starts. This parameter
            must be in the format: 'dd-mm-yyyy hh:mm'.
        duration : str
            Duration of the meeting in hours and minutes. This parameter must
            be in the format: 'hh:mm'.

        Returns
        -------
        None
            There is no return value on success, but the method modifies an
            instance variable: meetings.

        Exceptions
        ----------
        MeetingRoomTakenException
            Raised when there is a collision with already booked meeting.
            Additional information is passed to the Exception object.
        ValueError, AttributeError, IndexError, SyntaxError
            One of them is raised when the the input parameters do not conform
            to the required format.    
        """
 
        meeting_start = dt.datetime.strptime(date_time, '%d-%m-%Y %H:%M')
        duration = [int(n) for n in duration.split(':')]
        meeting_length = dt.timedelta(hours=duration[0], minutes=duration[1])
        for key, value in self.meetings.items():
            if self._is_overlap(key, key + value.duration,
                                meeting_start, meeting_start + meeting_length):    
                raise MeetingRoomTakenException(f'Meeting "{value.name}" '
                      f'on {key.date().strftime("%d %b %Y")} '
                      f'at {key.time().strftime("%H:%M")} '
                      f'will be using the room until '
                      f'{(key + value.duration).time().strftime("%H:%M")}')
        self.meetings[meeting_start] = MeetingRoom.MeetingInfo(name, 
                                                               meeting_length)

    def cancel_meeting(self, date_time):
        """Cancels meeting scheduled for a given date and time.

        Parameters
        ----------
        date_time : str
            Date of the meeting and the time when it starts. This parameter
            must be in the format: 'dd-mm-yyyy hh:mm'.

        Returns
        -------
        None
            There is no return value on success, but the method modifies an
            instance variable: meetings.

        Exceptions
        ----------
        MeetingNotFoundException
            Raised when there is no meeting scheduled for a given date and time.
            Additional information is passed to the Exception object.
        ValueError, AttributeError, IndexError, SyntaxError
            One of them is raised when the the input parameter does not conform
            to the required format.           
        """

        meeting_start = dt.datetime.strptime(date_time, '%d-%m-%Y %H:%M')
        if self.meetings.pop(meeting_start, None) is None:
            raise MeetingNotFound(f'There is no meeting in the room {self.room}'
                  f' scheduled for {meeting_start.date().strftime("%d %b %Y")}'
                  f' at {meeting_start.time().strftime("%H:%M")}')
  
    def daily_meetings(self, date):
        """Lists all meetings in the room during a given day.

        Parameters
        ----------
        date : str
            The date for which the listing is constructed. This parameter must
            be in the format: 'dd-mm-yyyy'.

        Returns
        -------
        string
            Printing ready formatted string showing the room name, date, and
            the list of all meetings for that day. The list includes meeting
            name and the times for its start and end.

        Exceptions
        ----------
        ValueError, AttributeError, IndexError, SyntaxError
            One of them is raised when the the input parameter does not conform
            to the required format. 
        """

        day = dt.datetime.strptime(date, '%d-%m-%Y')
        output = [f'Scheduled meetings in room {self.room} on '
                  f'{day.date().strftime("%d %b %Y")}:\n']
        for key, value in self.meetings.items():
            if key.date() == day.date():
                output.append(f'\t{value.name} {key.time().strftime("%H:%M")}'
                      f'--{(key + value.duration).time().strftime("%H:%M")}\n')
        if len(output) == 1:
            output.append('\tNo meetings')
        return ''.join(output).rstrip()

    def purge_past_meetings(self):
        """Purges old meetings from the booking schedule.

        Old meetings are those which were scheduled for dates before the current
        day, it means that they have already taken place.

        Parameters
        ----------
        no input parameters

        Returns
        -------
        integer
            The number of purged old meetings. This method modifies the instance
            variable: meetings.
        """

        today = dt.date.today()
        n = len(self.meetings)
        self.meetings = {key: value for key, value in self.meetings.items() 
                         if key.date() >= today}
        return n - len(self.meetings)


# example usage
if __name__ == '__main__':
    mr = MeetingRoom('Room 01A')
    print('Adding 5 meetings...')
    mr.add_meeting('Board meeting', '20-11-2018 10:30', '2:15')
    mr.add_meeting('Social club', '19-11-2018 16:45', '1:30')
    mr.add_meeting('Interview', '30-11-2018 9:00', '0:45')
    mr.add_meeting('Seminar', '29-11-2018 10:30', '3:00')
    mr.add_meeting('Presentations', '30-11-2018 11:30', '1:30')
    print(mr)
    print('Trying double booking...')
    try:
        mr.add_meeting('Training', '29-11-2018 12:00', '4:30')
    except MeetingRoomTakenException as e:
        print(e)
    print('\nListing meetings at a certain date...')
    print(mr.daily_meetings('30-11-2018'))
    print('\nCancelling 2 meetings...')
    try:
        mr.cancel_meeting('19-11-2018 16:45')
        print('OK')
        mr.cancel_meeting('1-11-2018 10:00')
    except MeetingNotFound as e:
        print(e)
    print('\nPurging old meetings...')
    print(f'Deleted {mr.purge_past_meetings()} meeting(s)')
    print('\nPrinting MeetingRoom object again...')
    print(mr)

