from threading import Thread
from multiprocessing import Process, Queue


def add(arguments_tuple):
    return sum(arguments_tuple)

 
def threadify(func, all_args):

    results = [0] * len(all_args)
    
    def one_task(func, idx, one_arg):
       results[idx] = func(one_arg)
       
    threads = []
    for i, arg in enumerate(all_args):
        # each thread modifies a single slot in the results list
        t = Thread(target=one_task, args=(func, i, arg))
        threads.append(t)   
        t.start()
        
    for t in threads:
        t.join()
   
    return results

   
def processify(func, all_args):

    # processes do not share global variables, queues can bo used
    # for communication between them
    queue = Queue()
    
    def one_task(func, idx, one_arg):
        # idx is the index of one_arg in all_args list
        queue.put((idx, func(one_arg)))
        
    processes = []
    for i, arg in enumerate(all_args):
        p = Process(target=one_task, args=(func, i, arg))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    results = []
    while not queue.empty():
        results.append(queue.get())
     
    # results are returned in the same order as arguments    
    return [item[1] for item in sorted(results)]

if __name__ == '__main__':
    arguments = [(2, 2), (3, 3), (4, 4)]
    print(threadify(add, arguments))
    print(processify(add, arguments))
    

