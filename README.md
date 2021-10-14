
# Ukrainian poems analyser

This project is dedicated to implementing a simple way to process specified poem and finding out its meter foot type. Available types are: choree, iamb, anapest, dactyl, amphibrach.


## Environment
Firstly, load into virtual environment and install the dependencies:
    
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

 
## How to launch
Simply run the `main.py`:

    $ python main.py

## Afternote
You can edit the `main.py` to either load a custom string or to load files from `poems` folder. You can also load your custom files by changing the way the `Poem` class is instantiated in `main.py`.