import time
from typing import Optional
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class PoemError(Exception): pass;

class TextStresser:
    '''Functionality to open selenium webdriver session.
    
    It loads the text stresser website and fetches the stressed version of input text.'''

    # Supress logs and hide selenium dev browser
    SILENT: bool = False
    # There isn't any normal API for this, so rely on parsing this exact resource to have a stressed version of text
    # Obviously, if there was a normal API it would perform way better, but we have what we have
    STRESSER_SITE: str = "https://slovnyk.ua/nagolos.php"

    def __init__(self) -> None:
        '''Initiate selenium webdriver for further crawling.'''

        op = webdriver.ChromeOptions()
        if self.SILENT:
           op.add_argument('headless')
        self.driver = webdriver.Chrome(options=op)

    def cleanup(self) -> None:
        '''Close the webdriver session.'''

        self.driver.close()

    def wait_for_result(self, retries: int = 3, timeout: int = 1) -> Optional[str]:
        '''Wait for the page to process the input and load the result text holder.'''

        while retries > 0:
            try:
                return self.driver.find_element_by_id('emph').get_attribute('textContent').strip()
            except NoSuchElementException:
                time.sleep(timeout)
                retries -= 1

        return None

    def stress(self, text: str) -> Optional[str]:
        '''Load the text stresser website, load the text there and fetch the results.'''

        self.driver.get(self.STRESSER_SITE)
        input_area = self.driver.find_element_by_tag_name('textarea')
        input_area.send_keys(text)
        submit_button = self.driver.find_element_by_xpath('//button[@type="submit"]')
        submit_button.click()
        stressed_text = self.wait_for_result()
        self.cleanup()

        return stressed_text

class Line:
    '''Functionality to load, process and store information about specific lines of text.'''

    # Available vowels - they signify syllables
    VOWELS: str = "АаОоУуЕеИиІіЯяЄєЇїЮю"
    # An ord of stress mark that signifies which syllable is stressed
    STRESS_MARK_ORD: int = 769

    def __init__(self, line: str) -> None:
        '''Load and process the line, then store it in corresponding fields.'''

        self.line = line
        self._make_reduced_line()
        self._generate_pattern()

    def _make_reduced_line(self):
        '''Reduce the loaded line to the list of syllables consisting of vowels.'''

        reduced_line = self.line
        allowed_letters = self.VOWELS + " " + chr(self.STRESS_MARK_ORD)
        for letter in reduced_line:
            if letter in allowed_letters:
                continue
            reduced_line = reduced_line.replace(letter, "")
        self.reduced_line = reduced_line
        print(self.reduced_line)

    def _generate_pattern(self):
        '''Process reduced line to generate its pattern.'''

        reversed_pattern = []
        for syllables in self.reduced_line.split(" ")[::-1]:
            syllables_count = len(syllables)
            skip_next_symbol = False
            for idx, symbol in enumerate(syllables[::-1]):
                if skip_next_symbol:
                    skip_next_symbol = False
                    continue
                if ord(symbol) != self.STRESS_MARK_ORD:
                    reversed_pattern.append(1)
                    continue
                skip_next_symbol = True
                if syllables_count == 1:
                    reversed_pattern.append(2)
                elif syllables_count == 2:
                    if idx == 0:
                        reversed_pattern.append(4)
                    else:
                        reversed_pattern.append(3)
                elif syllables_count > 2:
                    reversed_pattern.append(5)
                else:
                    reversed_pattern.append(0)

        self.pattern = "".join(str(x) for x in reversed_pattern[::-1])
        print(self.pattern)

class Poem:
    '''Wrapper to load and process the poem.'''

    def __init__(self, text: str = None, file: str = None) -> None:
        '''Load the text of the poem and process it.'''

        if text is not None:
            self.text = text
        elif file is None:
            self.text = self._readfile(file)
        else:
            raise PoemError("You should specify either text or file argument.")

        self.text_stresser = TextStresser()
        self.lines = []
        self._process_text()
        self._process_lines()

    def _process_text(self) -> None:
        '''Get the stressed version of the loaded text.'''

        self.stressed_text = self.text_stresser.stress(self.text) or self.text

    def _process_lines(self) -> None:
        '''Process the stressed version of loaded text line by line.'''

        for line in self.stressed_text.split("\n"):
            self.lines.append(Line(line))


    def _readfile(filename: str) -> str:
        '''Load text from file.'''

        with open(filename, "r") as f:
            return f.read()

    def show_text(self) -> None:
        '''Print out the loaded text.'''

        print(self.text)


def main() -> None:
    '''Main function for the program.'''

    text = "Ти не дивись, що буде там"
    p = Poem(text=text)
    p.show_text()


if __name__ == "__main__":
    main()