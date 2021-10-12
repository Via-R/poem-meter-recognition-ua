class PoemError(Exception): pass;

class TextStresser:
    def __init__(self) -> None:
        pass

    def stress(self, text):
        return text

class Line:
    vowels = "АаОоУуЕеИиІіЯяЄєЇїЮю"
    stressed_vowels = "А́а́Е́е́Є́є́И́и́І́і́Ї́ї́О́о́У́у́Ю́ю́Я́я́"

    def __init__(self, line: str) -> None:
        self.line = line
        self._make_reduced_line()
        self._generate_pattern()

    def _make_reduced_line(self):
        reduced_line = self.line
        allowed_letters = self.vowels + self.stressed_vowels + " "
        for letter in reduced_line:
            if letter in allowed_letters:
                continue
            reduced_line = reduced_line.replace(letter, "")
        self.reduced_line = reduced_line
        print(self.reduced_line)

    def _generate_pattern(self):
        pattern = []
        for syllables in self.reduced_line.split(" "):
            syllables_count = len(syllables)
            for idx, vowel in enumerate(syllables):
                if vowel not in self.stressed_vowels:
                    pattern.append(1)
                    continue
                if syllables_count == 1:
                    pattern.append(2)
                elif syllables_count == 2:
                    if idx == 0:
                        pattern.append(3)
                    else:
                        pattern.append(4)
                elif syllables_count > 2:
                    pattern.append(5)
                else:
                    pattern.append(0)

        self.pattern = "".join(str(x) for x in pattern)
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
        self.stressed_text = self.text_stresser.stress(self.text)

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