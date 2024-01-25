# # Alphabet
# LETTER = [chr(x) for x in range(ord('a'), ord('z') + 1)] + [chr(x) for x in range(ord('A'), ord('Z') + 1)] + ['_']
# DIGIT = [chr(x) for x in range(ord('0'), ord('9') + 1)]
# SPACE = [chr(x) for x in [9, 10, 13, 32]]
# ANY_CHAR = [chr(x) for x in range(32, 256)]
#
# # Token types
# DELIMITER = SPACE
# KEYWORDS = ['OR', 'DIV', 'MOD', 'AND', 'NOT', 'READ', 'WRITE']
# SPECIAL_SYMBOLS = [':=', '(', ')', ';', '+', '-', '*']
# ADDITIONAL_SYMBOLS = []
#
# # Symbol table
# symbol_table = {}
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
#     current_token = ""
#     comment = False
#
#     for i in code:
#         if i == "#":
#             comment = True
#         elif i == "\n":
#             tokens.append(Token("NewLine"))
#             comment = False
#         elif not comment and (i.isalnum() or i == "_"):
#             current_token += i
#         elif i == ":":
#             tokens.append(Token("SpecialSymbol", ":="))
#         elif current_token:
#             if current_token.upper() in KEYWORDS:
#                 tokens.append(Token("Keyword", current_token.upper()))
#             elif current_token.isnumeric():
#                 tokens.append(Token("Number", int(current_token)))
#             else:
#                 tokens.append(Token("Ident", current_token))
#             current_token = ""
#
#         if i in SPECIAL_SYMBOLS:
#             tokens.append(Token("SpecialSymbol", i))
#         elif i not in LETTER and i not in DIGIT and i not in SPACE:
#             if i != ":" and i != "=":
#                 ADDITIONAL_SYMBOLS.append(i)
#     return tokens
#
#
# # Parser
# class Parser:
#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.current_index = 0
#
#     def parse_code(self):
#         while self.current_index < len(self.tokens):
#             self.parse_operator()
#
#     def parse_operator(self):
#         token = self.tokens[self.current_index]
#
#         if token.token_type == "Keyword" and token.value == "READ":
#             self.match("Keyword")
#             token_id = self.tokens[self.current_index].value
#             self.match("Ident")
#
#             # Check if the identifier is already in the symbol table
#             if token_id not in symbol_table:
#                 symbol_table[token_id] = {"type": "int", "scope": "global"}
#             else:
#                 # Raise an exception if the variable is already declared
#                 raise Exception(f"Semantic error -> Variable '{token_id}' already declared.")
#
#         elif token.token_type == "Keyword" and token.value == "WRITE":
#             self.match("Keyword")
#             self.parse_expression()
#
#         elif token.token_type == "Ident":
#             token_id = self.tokens[self.current_index].value
#
#             self.match("Ident")
#             self.match("SpecialSymbol")
#             self.parse_expression()
#
#             # Check if the identifier is already in the symbol table
#             if token_id not in symbol_table:
#                 symbol_table[token_id] = {"type": "int", "scope": "global"}
#             else:
#                 raise Exception(f"Semantic error -> Variable '{token_id}' not declared.")
#
#         elif token.token_type == "SpecialSymbol" and token.value == ";":
#             self.match("SpecialSymbol")
#
#         elif token.token_type == "NewLine":
#             self.match("NewLine")
#
#         else:
#             self.panic()
#
#     def parse_expression(self):
#         self.parse_term()
#         while self.tokens[self.current_index].value in ["+", "-"]:
#             self.match("SpecialSymbol")
#             self.parse_term()
#
#     def parse_term(self):
#         self.parse_factor()
#         while self.tokens[self.current_index].value in ["*", "DIV", "MOD", "AND"]:
#             self.match("SpecialSymbol")
#             self.parse_factor()
#
#     def parse_factor(self):
#         token = self.tokens[self.current_index]
#
#         if token.value == "(":
#             self.match("SpecialSymbol")
#             self.parse_expression()
#             self.match("SpecialSymbol")
#         elif token.token_type == "Keyword" and token.value == "NOT":
#             self.match("Keyword")
#             self.parse_factor()
#         elif token.token_type == "Number" or token.token_type == "Ident":
#             # Additional check if the identifier is in the symbol table
#             if token.token_type == "Ident" and token.value not in symbol_table:
#                 raise Exception(f"Error: Variable '{token.value}' not declared.")
#             self.match(token.token_type)
#         else:
#             self.panic()
#
#     def match(self, expected_type):
#         token = self.tokens[self.current_index]
#
#         if token.token_type == expected_type:
#             self.current_index += 1
#         else:
#             self.panic()
#
#     def panic(self):
#         raise Exception(f"Parser error -> Unexpected token: {self.tokens[self.current_index]}")
#
#
# # Code Generator
# class CodeGenerator:
#     def __init__(self, symbol_table):
#         self.symbol_table = symbol_table
#
#     def generate_code(self, operator, *operands):
#         if operator == "READ":
#             variable = operands[0]
#             return f"mov eax, {variable}\n" \
#                    f"call input\n"
#
#         elif operator == "WRITE":
#             expression = operands[0]
#             return f"mov eax, {expression}\n" \
#                    f"call output\n"
#
#         elif operator == ":=":
#             target_variable, source = operands
#             return f"mov {target_variable}, {source}\n"
#
#         elif operator in ["+", "-", "*", "DIV", "MOD", "AND"]:
#             op1, op2 = operands
#             if operator == "DIV":
#                 # Handle division separately to avoid integer overflow issues
#                 return f"mov eax, {op1}\n" \
#                        f"cdq\n" \
#                        f"idiv {op2}\n"
#             elif operator == "MOD":
#                 return f"mov eax, {op1}\n" \
#                        f"cdq\n" \
#                        f"idiv {op2}\n" \
#                        f"mov eax, edx\n"
#             else:
#                 # Handle other arithmetic and logical operations
#                 asm_operator = {"+": "add", "-": "sub", "*": "imul", "AND": "and"}[operator]
#                 return f"mov eax, {op1}\n" \
#                        f"{asm_operator} eax, {op2}\n"
#
#         else:
#             raise Exception(f"Code generation error -> Unknown operator: {operator}")
#
#
# # Example source code
# example_code = """
# Read A;
# Read B;
# Read C;
# D := (A + B) * C;
# Write D;
# """
#
# # Get lexer result
# lexer_result = lexer(example_code)
#
# # Display the tokens from lexer
# [print(x) for x in lexer_result]
#
# # Display additional symbols
# if ADDITIONAL_SYMBOLS:
#     print(f"...\nUnexpected additional symbols -> {ADDITIONAL_SYMBOLS}\n...")
#
# # Test the parser
# parser = Parser(lexer_result)
# parser.parse_code()
#
# # Display the symbol table
# print("\nSymbol Table:")
# x = [print(f"{k}: {v}") for k, v in symbol_table.items()]
#
#
# # Code generation
# code_generator = CodeGenerator(symbol_table)
# assembly_code = ""
#
# i = 0
# while i < len(lexer_result):
#     token = lexer_result[i]
#
#     if token.token_type == "Keyword" and token.value in ["READ", "WRITE"]:
#         # Handle READ and WRITE operations
#         if token.value == "READ":
#             variable = lexer_result[i + 1].value
#             assembly_code += code_generator.generate_code(token.value, variable)
#             i += 2  # Skip the variable name
#         elif token.value == "WRITE":
#             i += 1  # Move to the next token
#             expression = lexer_result[i].value
#             i += 1  # Move to the next token after the expression
#             while i < len(lexer_result) and lexer_result[i].value in ["+", "-", "*", "DIV", "MOD", "AND"]:
#                 operator = lexer_result[i].value
#                 i += 1  # Move to the next token
#                 operand = lexer_result[i].value
#                 i += 1  # Move to the next token after the operand
#                 expression += f" {operator} {operand}"
#             assembly_code += code_generator.generate_code(token.value, expression)
#
#     elif token.token_type == "Ident":
#         # Handle variable assignments
#         target_variable = token.value
#         i += 1  # Move to the next token
#
#         if i < len(lexer_result) and lexer_result[i].token_type == "SpecialSymbol" and lexer_result[i].value == ":=":
#             i += 1  # Skip the :=
#             if lexer_result[i].value == "(":
#                 i += 1  # Move to the next token after "("
#                 expression = "("
#                 while i < len(lexer_result) and lexer_result[i].value != ";":
#                     expression += f" {lexer_result[i].value}"
#                     i += 1
#                 expression += ")"
#                 assembly_code += code_generator.generate_code(":=", target_variable, expression)
#             else:
#                 expression = lexer_result[i].value
#                 i += 1  # Move to the next token after the expression
#                 while i < len(lexer_result) and lexer_result[i].value in ["+", "-", "*", "DIV", "MOD", "AND"]:
#                     operator = lexer_result[i].value
#                     i += 1  # Move to the next token
#                     operand = lexer_result[i].value
#                     i += 1  # Move to the next token after the operand
#                     expression += f" {operator} {operand}"
#                 assembly_code += code_generator.generate_code(":=", target_variable, expression)
#
#     elif token.token_type == "SpecialSymbol" and token.value == ";":
#         i += 1  # Move to the next token
#
#     elif token.token_type == "NewLine":
#         i += 1  # Move to the next token
#
#     else:
#         i += 1  # Skip other tokens
#
# # Display the generated assembly code
# print("\nGenerated Assembly Code:")
# print(assembly_code)
