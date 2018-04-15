import glob
from threading import Thread
from queue import Queue

def file_word_count(filename, q=None):
    with open(filename, 'r') as input_file:
        words = sum(len(line.split()) for line in input_file)
    if q is None:
        return words
    else:
        q.put(words)

def count_words_sequential(pathname):
    """ Counting words -- sequential version
    """
    return sum(file_word_count(text_file) for text_file in glob.glob(pathname))

def count_words_threaded(pathname):
    """ Counting words -- threaded version
    """
    threads = []
    fifo = Queue()
    total_words = 0
    for text_file in glob.glob(pathname):
        t = Thread(target=file_word_count, args=(text_file, fifo))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    while not fifo.empty(): # all threads finished, queue not changes anymore
        total_words += fifo.get()
    return total_words

    

