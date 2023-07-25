# written by ME :)

####################################################################################
# IMPORT LIBRARIES

import PySimpleGUI as sg
import time
import os
import resources.ai_functions as ai
import resources.thread_runner as tr
import resources.app_runner as ar
import queue

# print verbose activates the print statements in the app threads
print_verbose = True


# check if generated_images directory is created, and, if not,
# creates the directory
if not os.path.exists('resources/generated_images/'):
    os.mkdir('resources/generated_images/')



####################################################################################
# DEFINE APP WINDOW CLASS

# class defining the GUI window and contains its functions
class app_window():

    # initialize the class with the pySimpleGUI window and the message queue
    def __init__(self, window, queue):

        # find the highest existing number in generated_images directory and
        # initializes n to one greater than it
        self.n = ai.return_max_n('resources/generated_images/') + 1

        self.window = window
        self.queue = queue
        self.breakflag = False
        self.bpress = 0

        self.check = False

    # define function that runs in the thread
    def run_app(self):

        # run the GUI thread
        while True:
            
            # initialize case to -10, the neutral case
            case = -10

            # initialize the prompt to a zero-length string
            prompt = ''

            # check GUI for updated values or events
            # valid events are button presses, valid values are prompts
            event, values = self.window.read(timeout=10)

            # if the 'generate' button is pressed, enter this block
            if event == "-GENERATE-":

                if print_verbose: ar.print_green('entered case 0')

                # as long as the prompt is not non-zero, and another button is not
                # pressed, enter this block
                if not values['-PROMPT-'] == '' and self.bpress == 0:
                    
                    # change text on 'generate' button to 'loading...'
                    self.window['-GENERATE-'].update("loading...")
                    # refresh window, updating the graphics
                    self.window.refresh()
                    
                    # set case to zero and the prompt to whatever string is in text box
                    case = 0
                    prompt = values['-PROMPT-']
                    
                    # incriment n, inform the class a button was pressed, and
                    # set variable to check for updated image to 'true'
                    self.n += 1
                    self.bpress = 1
                    self.check = True
                    
                else:
                    # if text box is empty or if another button was pressed, pass
                    pass
            
            
            # if the 'unzoom' button is pressed, enter this block
            elif event == "-UNZOOM-":
                if print_verbose: ar.print_green('entered case 1')

                # as long as the prompt is not non-zero, and another button is not
                # pressed, enter this block
                if os.path.isfile('resources/generated_images/img' + str(self.n-1) + '.png') and self.bpress == 0:
                    
                    # change text on 'unzoom' button to 'loading...'
                    self.window['-UNZOOM-'].update("loading...")
                    # refresh window, updating the graphics
                    self.window.refresh()
                    
                    # set case to one and the prompt to whatever string is in text box
                    case = 1
                    prompt = values['-PROMPT-']
                    
                    # incriment n, inform the class a button was pressed, and
                    # set variable to check for updated image to 'true'
                    self.n += 1
                    self.bpress = 2
                    self.check = True
                    
                else:
                    # if text box is empty or if another button was pressed, pass
                    pass
            
            # if the 'x' in the top right of the GUI is pressed, enter this block
            elif event == sg.WIN_CLOSED:

                if print_verbose: ar.print_green('entered case -9999')
                # set case to -9999
                case = -9999
                # update the queue
                self.queue.put({'case': case, 'n': self.n-1, 'prompt': prompt})

                break
            
            
            # update queue with new case, n, and prompt for thread 2 to receive
            self.queue.put({'case': case, 'n': self.n-1, 'prompt': prompt})

            # if the image corresponding to the current value of 'n' exists and the variable to check
            # for the updated variable is true, enter this block
            if os.path.isfile('resources/generated_images/img' + str(self.n-1) + '.png') and self.check == True:
                if print_verbose: ar.print_green('image found at location, updating window...')
                
                # pause for a moment, as the file is created before the image is fully written 
                # to the disk
                time.sleep(1.0)

                # reset 'generate' and 'unzoom' buttons
                self.window['-GENERATE-'].update("generate image")
                self.window['-UNZOOM-'].update("unzoom")

                # update the image to the current value of 'n'
                # (it's a try/except because it doesn't work without it
                # even though that makes no sense if you think about it)
                try:    self.window['-IMAGE-'].update(ar.makeItFit('resources/generated_images/img' + str(self.n-1) + '.png'))
                except: pass

                # reset button press indicating no buttons are being pressed
                self.bpress = 0

                # refresh window, updating the graphics
                self.window.refresh()

                # no longer have to check for new image
                self.check = False

                if print_verbose: ar.print_green('window refreshed\n\n')

            # pause loop for 1ms
            time.sleep(0.01)

    # define the function that executes upon exception encountered during runtime 
    def err(self):
        if print_verbose: ar.print_green('closing window')

        # if an error is encountered in the thread, close window and return 0
        self.window.close()
        return 0



####################################################################################
# DEFINE APP REQUESTS AND EVENTS CLASS

class requests_and_events_parser():

    # initialize the class with the message queue
    def __init__(self, queue):
        self.queue = queue

    # define function that runs in the thread
    def run_parse(self):

        # run the events parser
        while True:

            # check latest contents of queue
            requests = self.queue.get()

            # if the case is -9999 from the queue, enter this block
            if requests['case'] == -9999:
                if print_verbose: ai.print_red('received case -9999\n')

                # end the thread
                break
            
            # if the case is 0 from the queue, enter this block
            elif requests['case'] == 0:
                if print_verbose: ai.print_red('received case 0\n')
                
                # generate an image response given the prompt from the queue,
                # and save it to an image name correponding to 'n'
                _, _ = ai.generate_response_image(requests['prompt'], requests['n'])
            
            # if the case is 1 from the queue, enter this block
            elif requests['case'] == 1:
                if print_verbose: ai.print_red('received case 1\n')

                # generate an image response given the prompt from the queue,
                # and save it to an image name correponding to 'n'
                _ = ai.perturb_image('resources/generated_images/img' + str(requests['n']-1) + '.png', requests['prompt'], requests['n'])
            
            else:
                # if any other case, pass
                pass
            
            # pause for 1ms
            time.sleep(0.01)

    # define the function that executes upon exception encountered during runtime 
    def err(self):
        return 0



####################################################################################
# SET UP THE APP

# initialize the queue for thread-to-thread communication
if print_verbose: print('building queue')
queue = queue.Queue()

# define the app thread and the events parser thread classes
app = app_window(ar.window, queue)
rqs = requests_and_events_parser(queue)

# define the app thread and events parser threads
app_thread = tr.CustomThread(app.run_app, app.err)
rqs_thread = tr.CustomThread(rqs.run_parse, rqs.err)

# start the threads
if print_verbose: print('starting threads')
app_thread.start()
rqs_thread.start()

# join the threads once completed
if print_verbose: print('joining threads\n')
app_thread.join()
app_thread.join()
