# written by ME :)

####################################################################################
# IMPORT LIBRARIES

from threading import Thread

####################################################################################
# USAGE

'''
# import libraries
import thread_runner as tr
import queue
import time

# define class object for thread 1:
class app_1():

    # initialize with queue
    def __init__(self, queue):
        self.queue = queue
  
    # define run function to execute in thread
    def run_function(self):
    
        for i in range(10):
        
            print('thread 1 sending value ' + str(i) + ' to thread 2')
            self.queue.put({'value': i}) 

            time.sleep(0.05)

        return 0

    # define error function to execute on exception
    def err_function(self):
        return -1

      
# define class object for thread 2:
class app_2():
 
    # initialize with queue
    def __init__(self, queue):
        self.queue = queue
  
    # define run function to execute in thread
    def run_function(self):
    
        while True:
            requests = self.queue.get()

            value = requests['value']
            result = value**2

            print('thread 2 received value ' + str(value) + ', result is ' + str(result) + '\n')

            if value == 9:
                return 0

    # define error function to execute on exception
    def err_function(self):
        return -1

# initialize queue for thread-to-thread communication
q = queue.Queue()

# construct the two apps with the class
app_1_functions = app_1(q)
app_2_functions = app_2(q)

# define the custom threads
thread_1 = tr.CustomThread(app_1_functions.run_function, app_1_functions.err_function)
thread_2 = tr.CustomThread(app_2_functions.run_function, app_2_functions.err_function)

# start each thread
thread_1.start()
thread_2.start()

# join each thread for exit condition
thread_1.join()
thread_2.join()
'''

####################################################################################
# DEFINE CUSTOM THREAD

# custom thread that initializes with run function and 
# error handler. The run function executes in its thread,
# the error function executes if exception is encountered
class CustomThread(Thread):
    def __init__(self, function, error_handler):
        Thread.__init__(self)
        self.primary_function = function
        self.err = error_handler
        
    def run(self):
        try:
            self.primary_function()
        except Exception as e:
            print('encountered error: ' + str(e))
            self.err()