# written by ME :)

####################################################################################
# IMPORT LIBRARIES

import openai
import urllib.request
from PIL import Image
import os
from resources.app_runner import print_verbose


# define function that uses ANSI escape code to print in red
def print_red(text):
    # print('\033[0;31m' + text + '\033[0;0m')
    print(text)

# define openai key
f = open("key/openai_key.txt", "r")
openai.api_key = f.read()




####################################################################################
# DEFINE IMAGE GENERATION / MODIFICATION FUNCTIONS

# function that accepts a prompt and a value 'n', and saves the image
# to the generated_images directory under name img[n].png
def generate_response_image(prompt, n):

    # generate link to image on openai server given promopt
    if print_verbose: print_red('generating response ' + str(n) + ' given prompt: \'' + prompt + '\'')
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
    )

    # request image at link and save it as 'img[n].png'
    link_to_image = response["data"][0]["url"]
    if print_verbose: print_red('retrieving image at link: ' + link_to_image + '\n')
    urllib.request.urlretrieve(link_to_image, "resources/generated_images/img" + str(n) + ".png")
    
    return 0, 0

# function that adds a transparent mask around the boarder of image
# and has the ai fill in the tranparent mask given prompt. saves
# image as 'img[n].png'
def perturb_image(image, prompt, n):
    
    # add transparent mask around boarder of image 
    if print_verbose: print_red('adding mask to ' + image)
    add_mask(image)
    
    # genearte link to image on openai server given prompt and masked image
    if print_verbose: print_red('generating response ' + str(n) + ' given prompt: \'' + prompt + '\'')
    response = openai.Image.create_edit(
      image=open("resources/masking/masked.png", "rb"),
      mask=open("resources/masking/masked.png", "rb"),
      prompt=prompt,
      n=1,
      size="1024x1024"
    )
    
    # request image at link and save it as 'img[n].png'
    link_to_image = response["data"][0]["url"]
    if print_verbose: print_red('retrieving image at link: ' + link_to_image + '\n')
    urllib.request.urlretrieve(link_to_image, "resources/generated_images/img" + str(n) + ".png")
    
    return 0

# experimental function
def experimental_function(image1, image2, prompt, n):
    # defne mask, using transparent png in resources directory
    mask = Image.open('resources/masking/mask.png')

    w_l = 300
    h_l = 300
    # define image to be unzoomed, and resize it slightly smaller
    image_1 = Image.open(image1)
    image_1 = image_1.resize( (w_l, h_l), Image.LANCZOS)

    image_2 = Image.open(image2)
    image_2 = image_2.resize( (w_l, h_l), Image.LANCZOS)

    # define new image, which is the mask overlayed with the smaller image
    img_out = Image.new("RGBA", mask.size, (255, 255, 255, 0))
    w, h = mask.size
    img_out.paste(image_1, (int(w/2 - w_l - (w/2 - w_l)/2), int(h/2 - h_l/2)))
    img_out.paste(image_2, (int(w   - w_l - (w/2 - w_l)/2), int(h/2 - h_l/2)))

    # save masked image to upload for unzoom
    img_out.save('resources/masking/masked.png')

    # genearte link to image on openai server given prompt and masked image
    if print_verbose: print_red('generating response ' + str(n) + ' given prompt: \'' + prompt + '\'')
    response = openai.Image.create_edit(
        image=open("resources/masking/masked.png", "rb"),
        mask=open("resources/masking/masked.png", "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    # request image at link and save it as 'img[n].png'
    link_to_image = response["data"][0]["url"]
    if print_verbose: print_red('retrieving image at link: ' + link_to_image + '\n')
    urllib.request.urlretrieve(link_to_image, "resources/generated_images/img" + str(n) + ".png")
    
    return 0



####################################################################################
# DEFINE HELPER FUNCTIONS

# function to accept a prompt and show an image, used for debugging
def showMe(prompt, n):
    _, img = generate_response_image(prompt, n)
    img.show()

# function to accept an image and show a perturbed version, used for debugging
def showAgain(img, n):
    img = perturb_image(img, n)
    img.show()

# function to add transparent mask around boarder of image for unzoom
def add_mask(path):

    # defne mask, using transparent png in resources directory
    mask = Image.open('resources/masking/mask.png')
    
    # define image to be unzoomed, and resize it slightly smaller
    img = Image.open(path)
    img = img.resize( (600, 600), Image.LANCZOS)
    
    # define new image, which is the mask overlayed with the smaller image
    img_out = Image.new("RGBA", mask.size, (255, 255, 255, 0))
    w, h = mask.size
    img_out.paste(img, (int(w / 2 - 300), int(h / 2 - 300)))
    
    # save masked image to upload for unzoom
    img_out.save('resources/masking/masked.png')

# function that determines the largest number in the generated_images
# directory. Returns -1 if no images exists, returns the maximum number
# in directory if they do exist
def return_max_n(path):
    try:
        dir_list = os.listdir(path)
        nlist = []

        # append all file names to a list in whichever
        # directory was passed to it in 'path'
        for d in dir_list:

            # all characters of the file name
            # excluding the first 3, 'img', and the 
            # last 4, '.png', appending only 'n'
            nlist.append(int(d[3:][:-4]))

        # return the maximum value of list
        return max(nlist)
    except:

        # if no values to return, return -1
        return -1