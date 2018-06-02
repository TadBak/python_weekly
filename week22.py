import time

class TooSoonError(Exception):
    pass

def once_per_minute(func):
    
    def wrapper(*args, **kwargs):
        DELAY = 60
        if wrapper.timer_start is None:
            wrapper.timer_start = time.time()
            return func(*args, **kwargs)
        else:
            timer = time.time() - wrapper.timer_start
            if timer < DELAY:
                raise TooSoonError(f'Wait another {DELAY - timer} seconds')
            else:
                wrapper.timer_start = time.time()
                return func(*args, **kwargs)

    wrapper.timer_start = None
    return wrapper


@once_per_minute
def hello(name):
    return "Hello, {}".format(name)

for i in range(30):
    print(i)
    try:
        time.sleep(3)
        print(hello("attempt {}".format(i)))
    except TooSoonError as e:
        print("Too soon: {}".format(e))

