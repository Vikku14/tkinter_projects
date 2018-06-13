import threading
import time


def sleeper(n, name):
    print('Hi , I am {} Going to sleep'.format(name))
    time.sleep(n)
    print('I am waken after {} sec.s'.format(n))


thread = threading.Thread(target= sleeper, name= 'thread1',args=(3,"thread1"))
thread.start()
# thread.join()
print("hello")
print("hello")
print("hello")
print("hello")
print("hello")
