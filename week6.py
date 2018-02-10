import numpy as np
from collections import Counter

people = [{'name':'Reuven', 'age':47, 'hobbies':['Python', 'cooking', 'reading']},
          {'name':'Atara', 'age':16, 'hobbies':['horses', 'cooking', 'art']},
          {'name':'Shikma', 'age':14, 'hobbies':['Python', 'piano', 'cooking']},
          {'name':'Amotz', 'age':11, 'hobbies':['biking', 'cooking']}]

avg = np.mean([item['age'] for item in people if item['age']<25])
print(f'Average age of people under 25: {avg:.5}')

count = Counter([hobby for item in people for hobby in item['hobbies']])
print('All different hobbies:')
for hobby in list(count):
    print(f'\t{hobby}')

print('Number of people enjoying hobbies:')
for hobby, number in count.items():
    print(f'\t{hobby}\t{number}')

print('Three most common hobbies:')
for hobby, _ in count.most_common(3):
    print(f'\t{hobby}')

count2 = Counter([hobby for item in people for hobby in item['hobbies']
                 if len(item['hobbies'])>2])
print('Three most common hobbies amongst people with more than 2 hobbies:')
for hobby, _ in count2.most_common(3):
    print(f'\t{hobby}')






