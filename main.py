class PoemError(Exception): pass;

class Poem:
    def __init__(self, text = None, file = None) -> None:
        if text is not None:
            self.text = text
        elif file is None:
            self.text = self._readfile(file)
        else:
            raise PoemError("You should specify either text or file argument.")

    def _readfile(filename):
        with open(filename, "r") as f:
            return f.read()


def main():
    text = "Ти не дивись, що буде там"
    p = Poem(text=text)


if __name__ == "__main__":
    main()