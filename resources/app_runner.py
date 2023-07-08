# written by ME :)

####################################################################################
# IMPORT LIBRARIES

import PySimpleGUI as sg
from PIL import Image

# print verbose activates the print statements in the app threads
print_verbose = True


separator_bar = '`'*70
if print_verbose: print('\n\n' + separator_bar + '\n\t\t\tdrewsAI.py\n\n' + separator_bar)

# define function that uses ANSI escape code to print in green
def print_green(text):
    print('\033[0;32m' + text + '\033[0;0m')

# functin that resizes image to fit in app window, and saves
# output to 'show.png'
def makeItFit(path):

    if print_verbose: print_green('resizing image at ' + path)

    # read in image given file path
    img = Image.open(path)
    # resize image smaller to fit in app window
    smaller = img.resize( (400, 400), Image.LANCZOS)
    # save smaller image in resources directory as show.png,
    # which app window knows to display
    smaller.save('resources/masking/show.png')

    # return file path to resized image for app window
    return 'resources/masking/show.png'



####################################################################################
# DEFINE APP WINDOW LAYOUT

# sg.theme('DarktanBlue')
# sg.theme_button_color(('black', '#a63c35'))

# set themes for app window
if print_verbose: print_green('\n\ndetermining GUI theme')
sg.theme('DarkBlue1')
sg.theme_button_color(('black', '#c63c35'))

# define a blank frame to space out app window
def blank_frame():
    return sg.Frame("", [[]], pad=(5, 30), expand_x=True, expand_y=True, border_width=0)

# define app layout as two columns, containing input text
# box, buttons, and image display
if print_verbose: print_green('constructing GUI layout')
layout = [[
    sg.Column(
                [
                      # [blank_frame()],
                      
                      # [sg.Text('welcome to Drew\'s AI \U0001F920')],
                      # [sg.Text('let the AI know what you want to see.')],
                      
                      [blank_frame()],
                      
                      [   sg.Push(),
                          sg.Multiline('oil painting of guinea pig, wearing flowing tunic, in the style of a renaissance painting', 
                                       size=(50,10), font='Tahoma 13', key='-PROMPT-', autoscroll=True, no_scrollbar=True),
                          sg.Push()],
                      
                      [sg.Push(), sg.Button("generate image", key='-GENERATE-')],
                      
                      [sg.Push(), sg.Button("unzoom", key='-UNZOOM-')],
                      
                      [blank_frame()],
              
                  ], 
    
            scrollable=False, vertical_scroll_only = False),
        
    sg.Column([
                  [blank_frame()],
                  
                  [sg.Push(), sg.Image( makeItFit('resources/masking/icon.ico'), key='-IMAGE-' )],
                  
                  [blank_frame()],
          
              ], 
        
        scrollable=False, vertical_scroll_only = False),
    
    
    ],]

# define app window given the layout and themes
if print_verbose: print_green('constructing GUI window\n')
window = sg.Window("Drew\'s AI", layout, size=(950, 500), icon='resources/masking/icon.ico')