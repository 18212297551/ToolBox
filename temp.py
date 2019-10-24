import inspect
import functools
class T(object):
    def __init__(self):
        self.print_func()

    def print_func(self):
       info =  inspect.stack()[1]
       print(type(info[0]))


print(T().__module__)