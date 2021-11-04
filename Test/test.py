import threading
import time

def _thread_function1(arg1, arg2=None, arg3=None):
    g =  f'{arg1}, {arg2}, {arg3}'
    time.sleep(1)
    print(g)

def _thread_function2(arg1, arg2=None, arg3=None):
    g =  f'{arg1}, {arg2}, {arg3}'
    # time.sleep(1)
    print(g)


threading.Thread(target=_thread_function1, args=(77, 88, 39), name='thread_function').start()

threading.Thread(target=_thread_function2, args=(7, 81, 49), name='thread_function').start()