
def  parse_tokens(tokens_data):
    tokens = tokens_data['tokens']
    semantic_tokens = tokens_data['semantic_tokens']
    positions = tokens_data['token_position']

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
        if isinstance(semantic_tokens[t], CSharpElement):
            continue

        if class_identified and tokens[t] == '{':
            class_identified = False
            classinfo_expected = False

            class_end_position = tokens_data['enclosure_position'][t]

            print('Class identified: ' + class_name + " with baseclass/interfaces: " + str(classinfo_tokens))
            class_instance = CSharpClass(class_name, tokens[t:class_end_position], class_end_position)

            tokens_data = csharp_class_body_parser.parse_tokens(tokens_data, (t+1, tokens_data['enclosure_position'][t]), class_name, class_instance)
            class_instance.line_in_file = positions[start_class_pos][0]
            class_instance.methods_data = tokens_data['method_data']
            class_instance.base_info = classinfo_tokens
            classes_data.append(class_instance)
            for i in range(start_class_pos, t):
                semantic_tokens[i] = class_instance
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