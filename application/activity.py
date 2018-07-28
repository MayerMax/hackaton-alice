class AlreadyCompletedException(Exception):
    pass


class SimpleLevel:
    def __init__(self, word):
        self.word = word
        self.transformed = ['вверх', 'вниз']
        self.current_pos = 0

    def get_instruction(self):
        return self.transformed[self.current_pos]

    def is_correct_input(self, user_char):
        if self.current_pos >= len(self.word):
            raise AlreadyCompletedException()

        if self.word[self.current_pos] == user_char:
            self.current_pos += 1
            return True
        return False

    def is_completed(self):
        return self.current_pos >= len(self.word)

    def update_word(self, new_word):
        self.word = new_word
        self.current_pos = 0

    def restart(self, new_word):
        self.word = new_word
        self.current_pos = 0
        self.transformed = ['вверх', 'вниз']


class HardLevel:
    def __init__(self, word):
        self.word = word