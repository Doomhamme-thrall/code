import time

from memory_profiler import memory_usage


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        mem_usage_before = memory_usage(-1, interval=0.1, timeout=1)

        result = func(*args, **kwargs)

        mem_usage_after = memory_usage(-1, interval=0.1, timeout=1)
        elapsed_time = time.time() - start_time

        mem_usage = max(mem_usage_after) - min(mem_usage_before)

        print(f"function {func.__name__} cost {elapsed_time:.6f} seconds")
        print(f"function {func.__name__} used {mem_usage:.6f} MiB of memory")

        return result

    return wrapper
