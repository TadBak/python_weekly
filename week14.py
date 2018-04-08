import pickle
import datetime

class AddressBook:
    """ Simple address book with the option to restore from a specific
        timestamp.
    """
    def __init__(self):
        self._address_book = []
        self._stem = '/tmp/book_'
        self._actions = {'l': self.list_people,
                         'a': self.add_person,
                         'r': self.restore_book}

    def menu(self):
        while True:
            print('\n' + '-'*10 + ' Adress Book ' + '-'*10)
            print('\tq -> Quit from the program')
            print('\tl -> List all people in the address book')
            print('\ta -> Add a new person to the address book')
            print('\tr -> Restore the address book to the stage from a specific timestamp')
            choice = input('Please enter your choice: ')
            if choice == 'q':
                break
            else:
                if choice[0] in 'lar':
                    self._actions[choice[0]]()
                else:
                    print(f'Unknown option: {choice}')

        print('Good bye!')

    def list_people(self):
        for record in self._address_book:
            print(f"{record['first_name']} {record['last_name']}\t\t{record['email']}")

    def add_person(self):
        person = {}
        data = input("Please enter person's first name -> ")
        person['first_name'] = data
        data = input("please enter person's last name -> ")
        person['last_name'] = data
        data = input("Please enter person'e e-mail address -> ")
        person['email'] = data
        self._address_book.append(person)
        timestamp = '{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())
        with open(self._stem + timestamp, 'wb') as outfile:
            pickle.dump(self._address_book, outfile, pickle.HIGHEST_PROTOCOL)
        print(f'New person added, checkpoint with timestamp {timestamp} created')
 
    def restore_book(self):
        data = input('Please enter timestamp in the format\n'
                     'yyyy-mm-ddThh:mm:ss -> ')
        try:
            with open(self._stem + data, 'rb') as infile:
                self._address_book = pickle.load(infile)
            print(f'Address book restored to timestamp {data}')
        except FileNotFoundError:
            print(f'Checkpoint with the timestamp {data} not found')


if __name__ == '__main__':
    address_book = AddressBook()
    address_book.menu()

