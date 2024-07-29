import functools
import time

def caller(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k,v in kwargs.items()]
        res = func(*args, **kwargs)
        signature = ", ".join(args_repr + kwargs_repr)
        print(f'Calling {func.__name__}({signature})')
        return res
    return wrapper

def exec_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        tf = time.time()
        print("Execution time: " + str(round(tf - t0, 3)))
        return res
    return wrapper

def retry(num_retries):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(num_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed with error: {e}")
                    print(f"Result is {func()}")
            print(f"All {num_retries} attempts failed")
            return None
        return wrapper
    return decorator