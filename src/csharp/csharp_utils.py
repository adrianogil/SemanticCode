def is_valid_variable_name(token):
    return not is_special_token(token)

def is_valid_symbol(token, symbols):
    for s in symbols:
        if s == token:
            return True
    return False

def is_interface_keyword(token):
    return len(token) == 9 and \
        token[0] == 'i' and \
        token[1] == 'n' and \
        token[2] == 't' and \
        token[3] == 'e' and \
        token[4] == 'r' and \
        token[5] == 'f' and \
        token[6] == 'a' and \
        token[7] == 'c' and \
        token[8] == 'e'

def is_class_keyword(token):
    return len(token) == 5 and \
        token[0] == 'c' and \
        token[1] == 'l' and \
        token[2] == 'a' and \
        token[3] == 's' and \
        token[4] == 's'

def is_base_keyword(token):
    return len(token) == 4 and \
        token[0] == 'b' and \
        token[1] == 'a' and \
        token[2] == 's' and \
        token[3] == 'e'

def is_delegate_keyword(token):
    return len(token) == 8 and \
        token[0] == 'd' and \
        token[1] == 'e' and \
        token[2] == 'l' and \
        token[3] == 'e' and \
        token[4] == 'g' and \
        token[5] == 'a' and \
        token[6] == 't' and \
        token[7] == 'e'

def is_override_modifier(token):
    return len(token) == 8 and \
        token[0] == 'o' and \
        token[1] == 'v' and \
        token[2] == 'e' and \
        token[3] == 'r' and \
        token[4] == 'r' and \
        token[5] == 'i' and \
        token[6] == 'd' and \
        token[7] == 'e'

def is_virtual_modifier(token):
    return len(token) == 7 and \
        token[0] == 'v' and \
        token[1] == 'i' and \
        token[2] == 'r' and \
        token[3] == 't' and \
        token[4] == 'u' and \
        token[5] == 'a' and \
        token[6] == 'l'

def is_access_modifier(token):
    return is_public_modifier(token) or is_private_modifier(token) or is_protected_modifier(token)

def is_const_modifier(token):
    return len(token) == 5 and \
        token[0] == 'c' and \
        token[1] == 'o' and \
        token[2] == 'n' and \
        token[3] == 's' and \
        token[4] == 't'

def is_static_modifier(token):
    return len(token) == 6 and \
        token[0] == 's' and \
        token[1] == 't' and \
        token[2] == 'a' and \
        token[3] == 't' and \
        token[4] == 'i' and \
        token[5] == 'c'

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

def is_protected_modifier(token):
    return len(token) == 9 and \
        token[0] == 'p' and \
        token[1] == 'r' and \
        token[2] == 'o' and \
        token[3] == 't' and \
        token[4] == 'e' and \
        token[5] == 'c' and \
        token[6] == 't' and \
        token[7] == 'e' and \
        token[8] == 'd'

def is_special_token(char_content):
        return char_content == '.' or \
            char_content == ',' or \
            char_content == '{' or \
            char_content == '}' or \
            char_content == '(' or \
            char_content == ')' or \
            char_content == '#' or \
            char_content == '%' or \
            char_content == '+' or \
            char_content == '-' or \
            char_content == '/' or \
            char_content == '*' or \
            char_content == '<' or \
            char_content == '>' or \
            char_content == ';' or \
            char_content == '\"' or \
            char_content == '\''