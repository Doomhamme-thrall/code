import time

from memory_profiler import memory_usage


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        mem_before = memory_usage(-1, interval=0.1, timeout=1)

        result = func(*args, **kwargs)

        mem_after = memory_usage(-1, interval=0.1, timeout=1)
        end_time = time.time() - start_time

        mem = max(mem_after) - min(mem_before)

        print(f"{end_time:.6f} S")
        print(f"{mem:.6f} M")

        return result

    return wrapper
