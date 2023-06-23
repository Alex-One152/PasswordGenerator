import random
import string


class PasswordGenerator:
    def __init__(self, length=8, use_digits=True, use_letters=True, use_special_chars=True):
        self.length = length
        self.use_digits = use_digits
        self.use_letters = use_letters
        self.use_special_chars = use_special_chars

    def generate_password(self):
        characters = ''
        if self.use_digits:
            characters += string.digits
        if self.use_letters:
            characters += string.ascii_letters
        if self.use_special_chars:
            characters += string.punctuation

        if not characters:
            raise ValueError("At least one character set must be selected.")

        password = random.choices(characters, k=self.length)
        return ''.join(password)


if __name__ == '__main__':
    generator = PasswordGenerator()
    password = generator.generate_password()
    print(password)