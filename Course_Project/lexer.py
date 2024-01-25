# # Token types
# DELIMITER = " "
# KEYWORDS = ['OR', 'DIV', 'MOD', 'AND', 'NOT', 'READ', 'WRITE']
# SPECIAL_SYMBOLS = [':=', '(', ')', ';', '+', '-', '*']
#
#
# # Token class
# class Token:
#     def __init__(self, token_type, value=None):
#         self.token_type = token_type
#         self.value = value
#
#     def __str__(self):
#         return f'{self.token_type}->{self.value}' if self.value else f'{self.token_type}'
#
#
# # Lexer
# def lexer(code):
#     tokens = []
#     current_token = ''
#     comment = False
#
#     for i in code:
#         if i == '#':
#             comment = True
#         elif i == '\n':
#             tokens.append(Token('NewLine'))
#             comment = False
#         elif not comment and (i.isalnum() or i == '_'):
#             current_token += i
#         elif i == ":":
#             tokens.append(Token("SpecialSymbol", ":="))
#         elif current_token:
#             if current_token.upper() in KEYWORDS:
#                 tokens.append(Token('Keyword', current_token.upper()))
#             elif current_token.isnumeric():
#                 tokens.append(Token('Number', int(current_token)))
#             else:
#                 tokens.append(Token('Ident', current_token))
#             current_token = ''
#
#         if i in SPECIAL_SYMBOLS:
#             tokens.append(Token('SpecialSymbol', i))
#
#     return tokens
#
#
# # Example source code
# example_code = """
# Read A;
# B := A*2;
# Write B;
# """
#
# # Test the lexer
# lexer_result = lexer(example_code)
#
# # Display the tokens
# [print(x) for x in lexer_result]
