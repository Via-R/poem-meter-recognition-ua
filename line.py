from typing import Dict

from enums import MeterType, StressType

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
                if ord(symbol) != self.STRESS_MARK_ORD and syllables_count > 1:
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
