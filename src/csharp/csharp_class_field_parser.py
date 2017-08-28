import csharp_utils

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

class CSharpClassField:

    def __init__(self, csharp_field_name, class_id):
        self.field_name = csharp_field_name
        self.field_type = ''
        self.field_access_level = ''
        self.field_default_value = ''
        self.is_static = False
        self.class_id = class_id

    def add_entity(self, parser):
        self.parser = parser
        entity = parser.symbols.create_symbolic_entity(parser.get_file_path())
        entity.add_value('csharp_type', 'class_field')
        entity.add_value('class_id', self.class_id)
        entity.add_value('field_name', self.field_name)
        entity.add_value('field_type', self.field_type)
        entity.add_value('is_static', self.is_static)
        entity.add_value('field_access_level', self.field_access_level)
        entity.add_value('field_default_value', self.field_default_value)
        parser.symbols.add_entity(entity)
        self.entity = entity

# class_region = (token_start, token_end) of enclosure class
def parse_tokens(parser, class_region, class_name, class_entity_id):
    tokens_data = parser.tokens_data
    tokens = tokens_data['tokens']
    tokens_category = tokens_data['tokens_category']
    enclosure_position = tokens_data['enclosure_tokens']

    start_region = class_region[0]
    end_region = class_region[1]

    t = start_region

    member_start_pos = 0

    member_access_level = ''
    member_is_static = False
    member_is_const = False
    member_type = ''
    member_name = ''
    member_default_value = ''

    member_type_found = False
    member_name_found = False
    expected_default_value = False

    number_of_members = 0

    def create_field_instance(t):
        field_instance = CSharpClassField(member_name, class_entity_id)
        field_instance.field_type = member_type
        field_instance.field_access_level = member_access_level
        field_instance.field_default_value = member_default_value
        field_instance.line_in_file = tokens_data['tokens_position'][member_start_pos][0]
        field_instance.is_static = member_is_static

        field_instance.add_entity(parser)

    while t < end_region:

        if expected_default_value and tokens[t] == ';':
            print('\t +Member ' + member_name + " with type " + member_type + \
                " with default value " + member_default_value)

            create_field_instance(t)

            expected_default_value = False
            member_default_value = ''
            t = t + 1
        elif expected_default_value:
            member_default_value = member_default_value + tokens[t];
            t = t + 1
        elif tokens_category[t] != TokenCategory.Code:
            t = t + 1
        elif (t+4) < end_region and \
           tokens_category[t] == TokenCategory.Code and \
           tokens_category[t+1] == TokenCategory.Code and \
           tokens_category[t+2] == TokenCategory.Code and \
           tokens_category[t+3] == TokenCategory.Code and \
           csharp_utils.is_access_modifier(tokens[t]) and \
           csharp_utils.is_const_modifier(tokens[t+1]) and \
           (tokens[t+4] == ';' or tokens[t+4] == '='):
            member_access_level = tokens[t]
            member_is_const = True
            member_type = tokens[t+2]
            member_name = tokens[t+3]
            number_of_members = number_of_members + 1
            if tokens[t+4] == '=':
                expected_default_value = True
            t = t + 5
        elif (t+4) < end_region and \
             tokens_category[t] == TokenCategory.Code and \
             tokens_category[t+1] == TokenCategory.Code and \
             tokens_category[t+2] == TokenCategory.Code and \
             tokens_category[t+3] == TokenCategory.Code and \
             csharp_utils.is_access_modifier(tokens[t]) and \
             csharp_utils.is_static_modifier(tokens[t+1]) and \
             (tokens[t+4] == ';' or tokens[t+4] == '='):
            member_access_level = tokens[t]
            member_is_static = True
            member_type = tokens[t+2]
            member_name = tokens[t+3]
            number_of_members = number_of_members + 1
            if tokens[t+4] == '=':
                expected_default_value = True
            t = t + 5
        elif (t+4) < end_region and \
             tokens_category[t] == TokenCategory.Code and \
             tokens_category[t+1] == TokenCategory.Code and \
             tokens_category[t+2] == TokenCategory.Code and \
             tokens_category[t+3] == TokenCategory.Code and \
             csharp_utils.is_access_modifier(tokens[t]) and \
             csharp_utils.is_delegate_keyword(tokens[t+1]) and \
             (tokens[t+4] == ';' or tokens[t+4] == '='):
            member_access_level = tokens[t]
            member_is_static = True
            member_type = tokens[t+2]
            member_name = tokens[t+3]
            number_of_members = number_of_members + 1
            if tokens[t+4] == '=':
                expected_default_value = True
            t = t + 5
        elif (t+3) < end_region and \
             tokens_category[t] == TokenCategory.Code and \
             tokens_category[t+1] == TokenCategory.Code and \
             tokens_category[t+2] == TokenCategory.Code and \
             csharp_utils.is_access_modifier(tokens[t]) and \
             (tokens[t+3] == ';' or tokens[t+3] == '='):
            member_start_pos = t;
            member_access_level = tokens[t]
            member_is_static = True
            member_type = tokens[t+1]
            member_name = tokens[t+2]
            number_of_members = number_of_members + 1
            if tokens[t+3] == '=':
                expected_default_value = True
            else:
                expected_default_value = False
                create_field_instance(t+3)
                print('\t +Member ' + member_name + " with type " + member_type)
            t = t + 4
        elif (t+2) < end_region and \
             tokens_category[t] == TokenCategory.Code and \
             tokens_category[t+1] == TokenCategory.Code and \
             tokens_category[t+2] == TokenCategory.Code and \
             (tokens[t+2] == ';' or tokens[t+2] == '='):
            member_start_pos = t;
            member_access_level = 'default'
            member_is_static = False
            member_type = tokens[t]
            member_name = tokens[t+1]
            number_of_members = number_of_members + 1
            if tokens[t+2] == '=':
                expected_default_value = True
            else:
                expected_default_value = False
                create_field_instance(t+2)
                print('\t +Member ' + member_name + " with type " + member_type)
            t = t + 3
        else:
            t = t + 1

    if number_of_members > 0:
        print('\t +Member ' + member_name + " with type " + member_type)


