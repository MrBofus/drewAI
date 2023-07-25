# Welcome to drewAI

## Installing the code
Download the code by opening a console in the directory you want the code, and install by running:
```
git clone https://github.com/MrBofus/drewAI/
```
This will create a directory called 'drewAI' which will contain all the code neccessary to build the app.

## Building the App
There are two ways to build drewAI. The quickest method is running the python file, the more advanced is building an executable. To build drewAI as an executable, open a powershell window and run the following:
```
pyinstaller --onefile --noconsole .\drewsAI.py
```
This will create a folder called `dist` where it will put the executable. If the `resources` directory is not automatically copied over to `dist`, sure to copy and paste the `resources` directory to the `dist` folder. Run 'drewsAI.exe' to access the app.

Alternatively, the file `drewsAI.py` can be run from console.

## Usage
To use, first obtain an API key from the openAI website. To do this, go to www.openai.com and make an account. You can then generate your own API key. Next, create a folder called `key` in the parent `drewAI` directory. In this new folder, create a text file called `openai_key.txt` and paste the key into the file.

You can now run the code or the executable and access the AI.

There are two functions accessible---one is `generate image`, and the other is `unzoom`. Enter a prompt for the image you want and press the `generate image` button. An image is then generated and shown in the window. All generated images are saved to `resources/generated_images` with full resolution, so you can always access your generated images.

The other function, `unzoom`, 'unzooms' your generated image. Be sure to include a prompt that describes the entire scene, not just the unzoomed portion. This will use AI to fill in around the generated image, effectively "zooming out" from what was generated. All unzoomed images are also saved to `resources/generated_images`.
