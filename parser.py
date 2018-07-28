import os


class WordParser:
    def __init__(self, root_dir):
        self._root_dir = root_dir
        self.letters = self._load_letters()

    def _load_letter(self, file):
        with open(os.path.join(self._root_dir, file)) as f:
            lines = ['0{}0'.format(x) for x in f.read().split()]
            lines = [[int(x) for x in line] for line in lines]
            lines.insert(0, [0] * len(lines[0]))
            lines.append([0] * len(lines[0]))
            return lines

    def _load_letters(self):
        letters = {}
        for filename in os.listdir(self._root_dir):
            letters[os.path.splitext(filename)[0]] = self._load_letter(filename)
        return letters

    def parse_word(self, word):
        return [self.letters[symbol] for symbol in word.lower()]


if __name__ == '__main__':
    parser = WordParser(os.path.join('src', 'img'))
    letters = parser.parse_word('00')