import os

class FrameworkTest:
    test_file = 'testparse.cs'

    def __init__(self, parser):
        self.parser = parser

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.test_file = os.path.join(dir_path, self.test_file)

    def TestAll(self):
        self.TestTokenParse()

    def TestTokenParse(self):
        tokenized_data = self.parser.parse_file(self.test_file)

        return tokenized_data
