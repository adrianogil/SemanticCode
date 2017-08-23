import os

class FrameworkTest:

    def __init__(self, parser, file_name = 'testparse.cs'):
        self.parser = parser
        self.test_file = file_name

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.test_file = os.path.join(dir_path, self.test_file)

    def TestAll(self):
        self.TestTokenParse()

    def TestTokenParse(self):
        print('--- Start Testing - Token Parse ---')

        tokenized_data = self.parser.parse_file(self.test_file)

        print('--- Start End ----- Token Parse ---')

        return tokenized_data
