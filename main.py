import time
from typing import Optional
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class PoemError(Exception): pass;

class TextStresser:
    # Supress logs and hide selenium dev browser
    SILENT = False
    # There isn't any normal API for this, so rely on parsing this exact resource to have a stressed version of text
    # Obviously, if there was a normal API it would perform way better, but we have what we have
    STRESSER_SITE = "https://slovnyk.ua/nagolos.php"

    def __init__(self) -> None:
        op = webdriver.ChromeOptions()
        if self.SILENT:
           op.add_argument('headless')
        self.driver = webdriver.Chrome(options=op)

    def cleanup(self):
        self.driver.close()

    def wait_for_result(self, retries: int = 3, timeout: int = 1) -> Optional[str]:
        while retries > 0:
            try:
                return self.driver.find_element_by_id('emph').get_attribute('textContent').strip()
            except NoSuchElementException:
                time.sleep(timeout)
                retries -= 1

        return None

    def stress(self, text):
        self.driver.get(self.STRESSER_SITE)
        input_area = self.driver.find_element_by_tag_name('textarea')
        input_area.send_keys(text)
        submit_button = self.driver.find_element_by_xpath('//button[@type="submit"]')
        submit_button.click()
        stressed_text = self.wait_for_result()
        
        return stressed_text

class Line:
    VOWELS = "АаОоУуЕеИиІіЯяЄєЇїЮю"
    # stressed_vowels = "А́а́Е́е́Є́є́И́и́І́і́Ї́ї́О́о́У́у́Ю́ю́Я́я́"
    STRESS_MARK_ORD = 769

    def __init__(self, line: str) -> None:
        self.line = line
        self._make_reduced_line()
        self._generate_pattern()

    def _make_reduced_line(self):
        reduced_line = self.line
        allowed_letters = self.VOWELS + " " + chr(self.STRESS_MARK_ORD)
        for letter in reduced_line:
            if letter in allowed_letters:
                continue
            reduced_line = reduced_line.replace(letter, "")
        self.reduced_line = reduced_line
        print(self.reduced_line)

    def _generate_pattern(self):
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
    def __init__(self, text: str = None, file: str = None) -> None:
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
        self.stressed_text = self.text_stresser.stress(self.text) or self.text

    def _process_lines(self) -> None:
        for line in self.stressed_text.split("\n"):
            self.lines.append(Line(line))


    def _readfile(filename: str) -> str:
        with open(filename, "r") as f:
            return f.read()

    def show_text(self) -> None:
        print(self.text)


def main() -> None:
    text = "Ти не дивись, що буде там"
    p = Poem(text=text)
    p.show_text()


if __name__ == "__main__":
    main()