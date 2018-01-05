# travel data is stored in a dictionary, where the key is the visited country
# and the value is a list of towns within this country
travels = {}

while True:
    line = input('Tell me where you went: ')
    if not line:
        break
    if not ',' in line:
        print("That's not a legal city, country combination")
        continue
    city, country = [item.strip() for item in line.split(',', 1)]
    try:
        travels[country].append(city)
    except KeyError:
        travels[country] = [city]

print('\nYou visited:')
for country in sorted(travels.keys()):
    print('   {}'.format(country))
    counter = {city: travels[country].count(city) for city in travels[country]}
    for city in sorted(counter.keys()):
        if counter[city] > 1:
            print('      {0} ({1})'.format(city, counter[city]))
        else:
            print('      {}'.format(city))

