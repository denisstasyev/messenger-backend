import time
import random


def timer(function):
    def wrapper(*args, **kwargs):
        # print(args, kwargs)
        start_ts = time.time()
        result = function(*args, **kwargs)
        ts_end = time.time()
        print("Time of execution of function '{}' is {} ms."\
        .format(function.__name__, (ts_end-start_ts) * 1000))
        return result
    return wrapper


def sleeper(from_, to_):
    def sleeper_(function):
        def wrapper(*args, **kwargs):
            time_to_sleep = random.randint(from_, to_)
            print("We gonna sleep {} seconds.".format(time_to_sleep))
            time.sleep(time_to_sleep)
            result = function(*args, **kwargs)
            return result
        return wrapper
    return sleeper_


@sleeper(1, 3)  # sleeper - secondly
@timer  # timer will execute firstly
def foo(a, b):
    return a+b


if __name__ == "__main__":
    print(foo(b=10, a=5))