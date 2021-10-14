
# Ukrainian poems analyser

This project is dedicated to implementing a simple way to process specified poem and finding out its meter foot type. Available types are: choree, iamb, anapest, dactyl, amphibrach.
This README is stylised to be used with Linux and Mac OS, but similar instructions may be applied to run this project on Windows as well.
  
## Environment
Firstly, load into virtual environment and install the dependencies:
    
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

 You also need to have a `chromedriver` binary in your `$PATH`. You can read more about `chromedriver` [here](https://chromedriver.chromium.org/).
 
## How to launch
Simply run the `main.py`:

    $ python main.py

## Afternote
You can edit the `main.py` to either load a custom string or to load files from `poems` folder. You can also load your custom files by changing the way the `Poem` class is instantiated in `main.py`.