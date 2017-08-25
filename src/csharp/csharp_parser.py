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

    def parse_content(self, content):
        self.tokens_data = super(BasicCSharpParser, self).parse_content(content)
        csharp_importer_parser.parse_tokens(self)
        csharp_class_parser.parse_tokens(self)

