import time
from functools import*


start = time.time()

@lru_cache(maxsize=2)
def my_func(num):
    # time.sleep(2)
    lst = []
    for i in range(num):
        lst.append(i)
    return lst

my_func(50000000)

final = time.time()
print(f"Time taken : {round((final-start), 2)}")
