import requests
from bs4 import BeautifulSoup
import re

URLS = ['http://www.abc.net.au/news',
        'http://blog.lerner.co.il',
        'https://en.wikipedia.org/wiki/Python_(programming_language)'
       ]

def readability(url, dictionary):
    htm = requests.get(url, timeout=3)
    if htm.status_code != requests.codes.ok:
        return None
    soup = BeautifulSoup(htm.text, features='html.parser')
    # remove all scripts and CSSs
    for tag in soup(['script', 'style']):
        tag.decompose()
    # get text without tags and split it into words: \W+ means one or more
    # non-word characters, the resulting list is then converted into set 
    # in order to remove all duplicated words
    words = set(re.split('\W+', soup.get_text().strip()))
    # because an apostrophe is a non-word character the side effect is adding
    # a single letter 's' to the set, if words like it's, your's, etc. were
    # present in the document
    try:
        words.remove('s')
    except KeyError:
        pass
    # count number of words which are not in the dictionary
    not_found = len([item for item in words if item not in dictionary])
    # calculate the average number of characters in unique words
    length = round(sum([len(item) for item in words])/len(words))
    return not_found, length

if __name__ == '__main__':
    # load dictionary from file into set, not list, because lookup in sets
    # is faster than in lists
    dictionary = {line.strip() for line in open('/usr/share/dict/words')}
    for url in URLS:
        result = readability(url, dictionary)
        if result is None:
            print(f'URL: {url} is not accessible\n')
        else:
            print(f'URL: {url}\n\tnumber of words not in a dictionary: {result[0]}'
                  f'\n\taverage length of words: {result[1]} characters\n')

