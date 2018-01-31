import requests
import csv

url = 'https://gist.githubusercontent.com/reuven/77edbb0292901f35019f17edb9794358/raw/2bf258763cdddd704f8ffd3ea9a3e81d25e2c6f6/cities.json'
csv_file = 'largest_cities.csv'
output_fields = ['city', 'state', 'population', 'rank']

json_data = requests.get(url).json()
with open(csv_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=output_fields,
                            dialect='excel-tab', extrasaction='ignore')
    writer.writerows(json_data)



