import re

def process_log_file(file_name):
    pattern = r'(?P<ip_address>[\d\.]+) - - \[(?P<timestamp>.+)\] "(?P<request>GET .+?)"'
    log_data = []
    with open(file_name, 'r') as log_file:
        for line in log_file:
            matching = re.match(pattern, line)
            log_data.append(matching.groupdict())
    return log_data


if __name__ == '__main__':
    log_data = process_log_file('mini-access-log.txt')
    number_of_lines = len(log_data)
    print(f'Processed {number_of_lines} lines')
    print(f'Line 1:\n\tip_address: {log_data[0]["ip_address"]}\n\ttimestamp:'
          f' {log_data[0]["timestamp"]}\n\trequest: {log_data[0]["request"]}')
    print('. . .')
    print(f'Line {number_of_lines}:\n\tip_address: {log_data[-1]["ip_address"]}'
          f'\n\ttimestamp: {log_data[-1]["timestamp"]}\n\trequest: {log_data[-1]["request"]}')
          

        
            
