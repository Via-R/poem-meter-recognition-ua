import os
import time
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class PoemError(Exception): pass;

class StressType:
    '''Types of stresses in words for pattern generation.'''

    UNKNOWN = 0
    UNSTRESSED = 1
    ONE_SYLLABLE = 2
    TWO_SYLLABLES_FIRST_STRESSED = 3
    TWO_SYLLABLES_SECOND_STRESSED = 4
    MORE_THAN_TWO_SYLLABLES = 5

class MeterType:
    '''Types of metrical feet.'''

    IAMB = "ямб"
    CHOREE = "хорей"
    DACTYL = "дактиль"
    AMPHIBRACH = "амфібрахій"
    ANAPEST = "анапест"
    UNKNOWN = "невизначений"

class TextStresser:
    '''Functionality to open selenium webdriver session.
    
    It loads the text stresser website and fetches the stressed version of input text.'''

    # Hides selenium dev browser
    SILENT: bool = True
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
    STRESS_MARK: str = chr(STRESS_MARK_ORD)

    STRESS_TYPES: Dict[str, int] = {
        "unstressed"
    }

    def __init__(self, line: str) -> None:
        '''Load and process the line, then store it in corresponding fields.'''

        self.line = line
        self._make_reduced_line()
        self._generate_pattern()
        self._recognise_meter()

    def _make_reduced_line(self):
        '''Reduce the loaded line to the list of syllables consisting of vowels.'''

        reduced_line = self.line
        allowed_letters = self.VOWELS + " " + self.STRESS_MARK
        for letter in reduced_line:
            if letter in allowed_letters:
                continue
            reduced_line = reduced_line.replace(letter, "")
        self.reduced_line = reduced_line

    def _generate_pattern(self):
        '''Process reduced line to generate its pattern.'''

        if self.reduced_line.strip() == "":
            self.pattern = None
            return

        reversed_pattern = []
        for syllables in self.reduced_line.split(" ")[::-1]:
            syllables_count = self._get_letters_count(syllables)
            skip_next_symbol = False
            for idx, symbol in enumerate(syllables[::-1]):
                if skip_next_symbol:
                    skip_next_symbol = False
                    continue
                if ord(symbol) != self.STRESS_MARK_ORD:
                    reversed_pattern.append(StressType.UNSTRESSED)
                    continue
                skip_next_symbol = True
                if syllables_count == 1:
                    reversed_pattern.append(StressType.ONE_SYLLABLE)
                elif syllables_count == 2:
                    if idx == 0:
                        reversed_pattern.append(StressType.TWO_SYLLABLES_SECOND_STRESSED)
                    else:
                        reversed_pattern.append(StressType.TWO_SYLLABLES_FIRST_STRESSED)
                elif syllables_count > 2:
                    reversed_pattern.append(StressType.MORE_THAN_TWO_SYLLABLES)
                else:
                    reversed_pattern.append(StressType.UNKNOWN)

        self.pattern = "".join(str(x) for x in reversed_pattern[::-1])

    def _get_letters_count(self, word: str) -> int:
        '''Get amount of letters in the string, knowing that stress mark is counted as a separate letter.'''

        return len(word) - word.count(self.STRESS_MARK)

    def _recognise_meter(self):
        '''Make assumption on which metrical foot this line belongs to.'''

        if self.pattern is None:
            return

        two_syllables_types = (StressType.UNSTRESSED, StressType.ONE_SYLLABLE)

        # Checking for iamb
        for i in range(0, len(self.pattern), 2):
            if int(self.pattern[i]) not in two_syllables_types:
                break
        else:
            self.meter = MeterType.IAMB
            return

        # Checking for choree
        for i in range(1, len(self.pattern), 2):
            if int(self.pattern[i]) not in two_syllables_types:
                break
        else:
            self.meter = MeterType.CHOREE
            return

        three_syllables_types1 = (StressType.UNSTRESSED, StressType.ONE_SYLLABLE, StressType.TWO_SYLLABLES_FIRST_STRESSED)
        three_syllables_types2 = (StressType.UNSTRESSED, StressType.ONE_SYLLABLE, StressType.TWO_SYLLABLES_SECOND_STRESSED)
        
        # Checking for dactyl
        for i in range(1, len(self.pattern), 3):
            if int(self.pattern[i]) not in three_syllables_types1:
                break
        else:
            for i in range(2, len(self.pattern), 3):
                if int(self.pattern[i]) not in three_syllables_types2:
                    break
            else:
                self.meter = MeterType.DACTYL
                return

        # Checking for amphibrach
        for i in range(0, len(self.pattern), 3):
            if int(self.pattern[i]) not in three_syllables_types2:
                break
        else:
            for i in range(2, len(self.pattern), 3):
                if int(self.pattern[i]) not in three_syllables_types1:
                    break
            else:
                self.meter = MeterType.AMPHIBRACH
                return

        # Checking for anapest
        for i in range(0, len(self.pattern), 3):
            if int(self.pattern[i]) not in three_syllables_types1:
                break
        else:
            for i in range(1, len(self.pattern), 3):
                if int(self.pattern[i]) not in three_syllables_types2:
                    break
            else:
                self.meter = MeterType.ANAPEST
                return

        self.meter = MeterType.UNKNOWN

    def __str__(self) -> str:
        '''Override str method to show pattern on print().'''

        return f"{self.pattern}: {self.meter}"

class Poem:
    '''Wrapper to load and process the poem.'''

    def __init__(self, text: str = None, filename: str = None) -> None:
        '''Load the text of the poem and process it.'''

        if text is not None:
            self.text = text
        elif filename is not None:
            self.text = self._readfile(filename)
        else:
            raise PoemError("You should specify either text or file argument.")

        self.text_stresser = TextStresser()
        self.lines: List[Line] = []
        self._process_text()
        self._process_lines()
        self._calculate_results()

    def _process_text(self) -> None:
        '''Get the stressed version of the loaded text.'''

        self.stressed_text = self.text_stresser.stress(self.text) or self.text

    def _process_lines(self) -> None:
        '''Process the stressed version of loaded text line by line.'''

        for line in self.stressed_text.split("\n"):
            new_line = Line(line)
            if new_line.pattern is not None:
                self.lines.append(new_line)

    def _calculate_results(self) -> None:
        '''Get statistics from lines and make final assumption about meter foot of the poem.'''

        meters_found = {}

        for line in self.lines:
            if line.meter not in meters_found:
                meters_found[line.meter] = 0

            meters_found[line.meter] += 1

        self.meter = max(meters_found, key=meters_found.get)
        self.meter_probability = meters_found[self.meter] / len(self.lines)

    def _readfile(self, filename: str) -> str:
        '''Load text from file.'''

        if not os.path.exists(filename):
            raise PoemError("The specified filename doesn't exist.")

        with open(filename, "r") as f:
            return f.read()

    def show_text(self) -> None:
        '''Print out the loaded text.'''

        print(self.text)

    def show_patterns(self) -> None:
        '''Print out all processed patterns.'''

        print(*[line for line in self.lines], sep='\n')

    def show_meter_type(self) -> None:
        '''Shows final result of calculations.'''

        print(f"Віршовий розмір: {self.meter}, ймовірність {self.meter_probability}")


def main() -> None:
    '''Main function for the program.'''

    text = "Ти не дивись, що буде там"
    filename = 'choree.txt'
    p = Poem(filename=filename)
    p.show_meter_type()


if __name__ == "__main__":
    main()