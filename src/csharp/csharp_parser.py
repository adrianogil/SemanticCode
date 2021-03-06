import sys

import csharp_class_parser
import csharp_importer_parser

sys.path.append('framework')
import token_parser
import symbolic_data

class BasicCSharpParser(token_parser.TokenParser):
    def __init__(self, parse_behavior = None):
        super(BasicCSharpParser, self).__init__(parse_behavior)
        self.symbols = symbolic_data.SymbolicData()
        self.file_path = ''

    def get_file_path(self):
        return self.file_path

    def parse_file(self, csharp_file):
        self.file_path = csharp_file
        return super(BasicCSharpParser, self).parse_file(csharp_file)

    def parse_content(self, content):
        self.tokens_data = super(BasicCSharpParser, self).parse_content(content)
        self.tokens_data = csharp_importer_parser.parse_tokens(self)
        self.tokens_data = csharp_class_parser.parse_tokens(self)

        return self.tokens_data

