import sys

import csharp_class_parser

sys.path.append('framework')
import token_parser

class BasicCSharpParser(token_parser.TokenParser):
    def __init(self, parse_behavior = None):
        super(BasicCSharpParser, self).__init__(self, parse_behavior)

    def parse_content(self, content):
        tokens_data = super(BasicCSharpParser, self).parse_content(content)
        csharp_class_parser.parse_tokens(tokens_data)

