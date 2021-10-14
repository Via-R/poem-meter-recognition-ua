import os

from poem import Poem

def main() -> None:
    '''Main function for the program.'''

    # text = "Ти не дивись, що буде там"
    # p = Poem(text=text)
    
    poems_direcotry = 'poems'
    for filename in os.listdir(poems_direcotry):
        poem_file = os.path.join(poems_direcotry, filename)
        if os.path.isfile(poem_file) and poem_file.endswith('.txt'):
            print(f"{poem_file} | ", end='')
            p = Poem(filename=poem_file)
            p.show_meter_type()


if __name__ == "__main__":
    main()