import os
from typing import List

from stresser import TextStresser
from line import Line

class PoemError(Exception): pass;

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
