import pandas as pd

base_url = 'http://127.0.0.1:5000/'

def main_loop():
    print('Simple client for a directory monitoring service.')
    while True:
        print('\nMenu:\n\t0: Exit\n\t1: Take a snapshot of a directory\n\t'
              '2: Check for changes in a directory')
        choice = input('Please choose: ')
        try:
            menu = int(choice)
        except ValueError:
            print(f'Unrecognised option: {choice}')
            continue
        if menu == 0:
            break
        elif menu == 1:
            scan()
        elif menu == 2:
            rescan()
        else:
            print(f'Unrecognised option: {str(menu)}')
    print('Bye!')

def scan():
    directory = input('Directory to scan? ')
    url = base_url + 'scan/?' + directory
    ds = get_response(url)
    if ds is not None:
        print(ds['message'])
        if ds['status'] == 0:
            print(ds['pathname'] + '\n' + ds['timestamp'])
        
def rescan():
    directory = input('Directory to check? ')
    url = base_url + 'rescan/?' + directory
    ds = get_response(url)
    if ds is not None:  
        print(ds['message'])
        if ds['status'] == 0:
            print('of ' + ds['pathname'])
            print('on ' + ds['timestamp'])
            changes = (print_data(ds['data']['added'], 'Files added to the directory:')
                or print_data(ds['data']['removed'], 'Files removed from the directory:')
                or print_data(ds['data']['changed'], 'Files changed in the directory:'))
            if not changes:
                print('\tNo changes')

def get_response(url):
    try:
        series = pd.read_json(url, typ='series')
    except IOError:
        print('Server is not responding')
        return None
    return series

def print_data(data, msg):
    if data:
        print(msg)
        for item in data:
            print(f'\t{item}')
        return True
    return False


if __name__ == '__main__':
    main_loop()

