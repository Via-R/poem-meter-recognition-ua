class PoemError(Exception): pass;

class Line:
    vowels = "АаОоУуЕеИиІіЯяЄєЇїЮю"
    stressed_vowels = "А́а́Е́е́Є́є́И́и́І́і́Ї́ї́О́о́У́у́Ю́ю́Я́я́"

    def __init__(self, line: str) -> None:
        self.line = line
        self._make_reduced_line()

    def _make_reduced_line(self):
        reduced_line = self.line
        allowed_letters = self.vowels + self.stressed_vowels + " "
        for letter in reduced_line:
            if letter in allowed_letters:
                continue
            reduced_line = reduced_line.replace(letter, "")
        self.reduced_line = reduced_line
        print(self.reduced_line)

class Poem:
    def __init__(self, text: str = None, file: str = None) -> None:
        if text is not None:
            self.text = text
        elif file is None:
            self.text = self._readfile(file)
        else:
            raise PoemError("You should specify either text or file argument.")

        self.lines = []
        self._process_text()
        self._process_lines()

    def _process_text(self) -> None:
        pass

    def _process_lines(self) -> None:
        for line in self.text.split("\n"):
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