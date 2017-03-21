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

class DefaultParseBehavior:

    def is_escaped_string_element(self, line, j):
        if line[j] != '\'' and line[j] != '\"':
            return False
        if j == 0:
            return False
        escaped_string = False
        j = j - 1
        while j >= 0 and line[j] == '\\':
            escaped_string = not escaped_string
            j = j - 1
        return escaped_string

    def is_empty(self, char_content):
        return char_content == ' ' or char_content == '\n' or char_content == '\t'

    def is_opening_element(self, char_content, token_category):
        if char_content == '\"' or \
            char_content == '\'':
            return True
        return token_category == TokenCategory.Code and \
            (char_content == '{' or \
            char_content == '(' or \
            char_content == '[' )


    def is_enclosure_element(self, char_content, token_category):
        if char_content == '\"' or \
            char_content == '\'':
           return True
        return token_category == TokenCategory.Code and \
            (char_content == '}' or \
            char_content == ')' or \
            char_content == ']')

    def is_special_token(self, char_content):
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

    def is_inside_inline_comment(self, line, pos):
        line_size = len(line)
        return pos < line_size-2 and \
            line[pos] == '/' and \
            line[pos+1] == '/'

    def is_inside_stream_comment(self, line, pos):
        line_size = len(line)
        return pos < line_size-2 and \
            line[pos] == '/' and \
            line[pos+1] == '*'

    def is_outside_stream_comment(self, line, pos):
        line_size = len(line)
        return pos > 0 and \
            line[pos-1] == '*' and \
            line[pos] == '/'