import csharp_class_method_parser
import csharp_class_field_parser

class TokenCategory:
    '''
        Tokens categories:
        0 - code
        1 - string
        2 - commentary
    '''
    Code = 0
    String = 1
    Comment = 2

class CSharpClass():
    def __init__(self, class_name, base_info, line_in_file):
        self.class_name = class_name
        self.base_info = base_info
        self.line_in_file = line_in_file

    def add_entity(self, parser):
        self.parser = parser
        entity = parser.symbols.create_symbolic_entity(parser.get_file_path())
        entity.add_value('csharp_type', 'class')
        entity.add_value('class_name', self.class_name)
        entity.add_value('base_info', self.base_info)
        entity.add_value('line_in_file', self.line_in_file)
        parser.symbols.add_entity(entity)
        self.class_entity = entity

    def parse_class_body(self, class_region):
        class_entity_id = self.class_entity.id

        csharp_class_method_parser.parse_tokens(self.parser, class_region, self.class_name, class_entity_id)
        csharp_class_field_parser.parse_tokens(self.parser, class_region, self.class_name, class_entity_id)
        # csharp_class_property_parser.parse_tokens(self.parser, class_region, class_name, class_instance)

def  parse_tokens(parser):
    tokens_data = parser.tokens_data
    tokens = tokens_data['tokens']
    tokens_category = tokens_data['tokens_category']
    # print(str(tokens))

    tokens_category = tokens_data['tokens_category']
    positions = tokens_data['enclosure_tokens']

    print('charp_class_parser - ' + str(len(tokens)) + " tokens")

    total_tokens = len(tokens)

    classes_data = []

    class_name = ''

    class_identified = False
    classinfo_expected = False # A base class or an interface
    classinfo_identified = False

    classinfo_tokens = []

    start_class_pos = 0

    for t in range(1, total_tokens):
        # Can't consider importers inside strings
        if tokens_category[t] != TokenCategory.Code:
            continue

        if class_identified and tokens[t] == '{':
            class_identified = False
            classinfo_expected = False

            class_end_position = tokens_data['enclosure_tokens'][t]

            print('Class identified: ' + class_name + " with baseclass/interfaces: " + str(classinfo_tokens))
            class_instance = CSharpClass(class_name, classinfo_tokens, positions[start_class_pos])
            class_instance.add_entity(parser)
            class_instance.parse_class_body((t+1, tokens_data['enclosure_tokens'][t]))
            # class_instance.line_in_file = positions[start_class_pos][0]
            # class_instance.methods_data = tokens_data['method_data']
            # class_instance.base_info = classinfo_tokens

            # for i in range(start_class_pos, t):
            #     semantic_tokens[i] = class_instance
            class_name = ''
            classinfo_tokens = []

        elif class_identified and len(classinfo_tokens) > 0 and tokens[t] == ',':
            classinfo_expected = True
        elif class_identified and classinfo_expected:
            classinfo_tokens.append(tokens[t])
            classinfo_expected = False
        if class_identified and tokens[t] == ':':
            classinfo_expected = True
        elif t > 2 and is_access_modifier(tokens[t-2]) and is_class_keyword(tokens[t-1]):
            class_name = tokens[t]
            start_class_pos = t-2
            class_identified = True
        elif is_class_keyword(tokens[t-1]):
            class_name = tokens[t]
            start_class_pos = t-2
            class_identified = True

    tokens_data['classes'] = classes_data
    tokens_data['outline_data'] = classes_data

    return tokens_data

def is_access_modifier(token):
    return is_public_modifier(token) or is_private_modifier(token)

def is_public_modifier(token):
    return len(token) == 6 and \
        token[0] == 'p' and \
        token[1] == 'u' and \
        token[2] == 'b' and \
        token[3] == 'l' and \
        token[4] == 'i' and \
        token[5] == 'c'

def is_private_modifier(token):
    return len(token) == 7 and \
        token[0] == 'p' and \
        token[1] == 'r' and \
        token[2] == 'i' and \
        token[3] == 'v' and \
        token[4] == 'a' and \
        token[5] == 't' and \
        token[6] == 'e'

def is_class_keyword(token):
    return len(token) == 5 and \
        token[0] == 'c' and \
        token[1] == 'l' and \
        token[2] == 'a' and \
        token[3] == 's' and \
        token[4] == 's'