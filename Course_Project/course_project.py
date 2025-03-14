"""
* Simple-P-1 *
* Rumen Iliev *
* 2001261038 *
"""

# Alphabet
LETTER = [chr(x) for x in range(ord('a'), ord('z') + 1)] + [chr(x) for x in range(ord('A'), ord('Z') + 1)] + ['_']
DIGIT = [chr(x) for x in range(ord('0'), ord('9') + 1)]
SPACE = [chr(x) for x in [9, 10, 13, 32]]
ANY_CHAR = [chr(x) for x in range(32, 256)]

# Token types
DELIMITER = SPACE
KEYWORDS = ['OR', 'DIV', 'MOD', 'AND', 'NOT', 'READ', 'WRITE', "SKIP"]
SPECIAL_SYMBOLS = [':=', '(', ')', ';', '+', '-', '*']
ADDITIONAL_SYMBOLS = []

# Symbol table
symbol_table = {}


# Token class
class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f'{self.token_type}->{self.value}' if self.value else f'{self.token_type}'


# Lexer
def lexer(code):
    tokens = []
    current_token = ""
    comment = False

    for i in code:
        if i == "#":
            comment = True
        elif i == "\n":
            tokens.append(Token("NewLine"))
            comment = False
        elif not comment and (i.isalnum() or i == "_"):
            current_token += i
        elif i == ":":
            tokens.append(Token("SpecialSymbol", ":="))
        elif current_token:
            if current_token.upper() in KEYWORDS:
                tokens.append(Token("Keyword", current_token.upper()))
            elif current_token.isnumeric():
                tokens.append(Token("Number", int(current_token)))
            else:
                tokens.append(Token("Ident", current_token))
            current_token = ""

        if i in SPECIAL_SYMBOLS:
            tokens.append(Token("SpecialSymbol", i))
        elif i not in LETTER and i not in DIGIT and i not in SPACE:
            if i != ":" and i != "=":
                ADDITIONAL_SYMBOLS.append(i)
    return tokens


# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0

    def parse_code(self):
        while self.current_index < len(self.tokens):
            self.parse_operator()

    def parse_operator(self):
        token = self.tokens[self.current_index]

        if token.token_type == "Keyword":
            if token.value in ["READ", "WRITE", "OR", "DIV", "MOD", "AND", "NOT", "SKIP"]:
                self.parse_keyword_operator()
            else:
                self.panic()

        elif token.token_type == "Ident":
            self.parse_for_ident()

        elif token.token_type == "SpecialSymbol" and token.value == ";":
            self.match("SpecialSymbol")

        elif token.token_type == "NewLine":
            self.match("NewLine")

        else:
            self.panic()

    def parse_keyword_operator(self):
        token = self.tokens[self.current_index]

        if token.value == "READ":
            self.parse_read()
        elif token.value == "WRITE":
            self.parse_write()
        elif token.value == "SKIP":
            self.parse_skip()
        else:
            self.panic()

    def parse_read(self):
        self.match("Keyword")
        token_id = self.tokens[self.current_index].value
        self.match("Ident")

        # Check if the identifier is already in the symbol table
        if token_id not in symbol_table:
            symbol_table[token_id] = {"type": "int", "scope": "global"}
        else:
            # Raise an exception if the variable is already declared
            raise Exception(f"Semantic error -> Variable '{token_id}' already declared.")

    def parse_write(self):
        self.match("Keyword")
        self.parse_expression()

    def parse_or(self):
        self.match("Keyword")
        self.parse_expression()
        self.match("Keyword")
        self.parse_expression()

    def parse_div(self):
        self.match("Keyword")
        self.parse_expression()
        self.match("Keyword")
        self.parse_expression()

    def parse_mod(self):
        self.match("Keyword")
        self.parse_expression()
        self.match("Keyword")
        self.parse_expression()

    def parse_and(self):
        self.match("Keyword")
        self.parse_expression()
        self.match("Keyword")
        self.parse_expression()

    def parse_not(self):
        self.match("Keyword")
        self.parse_expression()

    def parse_skip(self):
        self.match("Keyword")
        self.current_index += 1

    def parse_for_ident(self):
        token_id = self.tokens[self.current_index].value
        self.match("Ident")
        self.match("SpecialSymbol")
        self.parse_expression()

        # Check if the identifier is already in the symbol table
        if token_id not in symbol_table:
            symbol_table[token_id] = {"type": "int", "scope": "global"}
        else:
            raise Exception(f"Semantic error -> Variable '{token_id}' not declared.")

    def parse_expression(self):
        self.parse_term()
        while self.tokens[self.current_index].value in ["+", "-"]:
            self.match("SpecialSymbol")
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.tokens[self.current_index].value in ["*", "DIV", "MOD", "AND", "OR"]:
            x = self.tokens[self.current_index].value
            if x == "*":
                self.match("SpecialSymbol")
                self.parse_factor()
            elif x in ["DIV", "MOD", "AND", "OR"]:
                self.match("Keyword")
                self.parse_factor()
            else:
                self.panic()

    def parse_factor(self):
        token = self.tokens[self.current_index]

        if token.value == "(":
            self.match("SpecialSymbol")
            self.parse_expression()
            self.match("SpecialSymbol")
        elif token.token_type == "Keyword" and token.value == "NOT":
            self.match("Keyword")
            self.parse_factor()
        elif token.token_type == "Number" or token.token_type == "Ident":

            # Additional check if the identifier is in the symbol table
            if token.token_type == "Ident" and token.value not in symbol_table:
                raise Exception(f"Error: Variable '{token.value}' not declared.")
            self.match(token.token_type)
        else:
            self.panic()

    def match(self, expected_type):
        token = self.tokens[self.current_index]

        if token.token_type == expected_type:
            self.current_index += 1
        else:
            self.panic()

    def panic(self):
        raise Exception(f"Parser error -> Unexpected token: {self.tokens[self.current_index]}")


# Code Generator
class CodeGenerator:
    def __init__(self, symbol_t):
        self.symbol_t = symbol_t

    def generate_code(self, x, *args):

        if x == "READ":
            return f"mov eax, {args[0]}\n" \
                   f"call input\n"

        elif x == "WRITE":
            return f"mov eax, {args[0]}\n" \
                   f"call output\n"

        elif x == ":=":
            return f"mov {args[0]}, {args[1]}\n"

        elif x in ["+", "-", "*", "DIV", "MOD", "AND"]:

            if x == "DIV":
                return f"mov eax, {args[0]}\n" \
                       f"cdq\n" \
                       f"idiv {args[1]}\n"

            elif x == "MOD":
                return f"mov eax, {args[0]}\n" \
                       f"cdq\n" \
                       f"idiv {args[1]}\n" \
                       f"mov eax, edx\n"
            else:
                asm_operator = {"+": "add", "-": "sub", "*": "imul", "AND": "and"}[x]
                return f"mov eax, {args[0]}\n" \
                       f"{asm_operator} eax, {args[1]}\n"
        else:
            raise Exception(f"Code generation error -> Unknown operator: {x}")


# Input your code here:
example_code = """
Read X;
Read Y;
Z := X + Y;
W := Z * 2;
P := W + 7;
Q := P DIV 3;
R := Q - 4;
S := R * X;
T := Y + S;
Write T;
"""


# Get lexer result
lexer_result = lexer(example_code)


print("...\nResult after lexical analysis:\n...")
[print(x) for x in lexer_result]


if ADDITIONAL_SYMBOLS:
    print(f"\n...\nUnexpected additional symbols -> {ADDITIONAL_SYMBOLS}\n...")


# Run the parser
parser = Parser(lexer_result)
parser.parse_code()


print("\n...\nSymbol Table:\n...")
[print(f"{k}: {v}") for k, v in symbol_table.items()]


code_generator = CodeGenerator(symbol_table)
assembly_code = ""

i = 0
while i < len(lexer_result):

    token = lexer_result[i]

    if token.token_type == "Keyword" and token.value == "READ":
        assembly_code += code_generator.generate_code(token.value, lexer_result[i + 1].value)
        i += 2

    elif token.token_type == "Keyword" and token.value == "WRITE":
        i += 1
        x = ""
        while i < len(lexer_result) and lexer_result[i].value != ";":
            x += f"{lexer_result[i].value} "
            i += 1
        assembly_code += code_generator.generate_code(token.value, x.strip())

    elif token.token_type == "Ident":
        token_value = token.value
        i += 1

        if i < len(lexer_result) and lexer_result[i].token_type == "SpecialSymbol" and lexer_result[i].value == ":=":
            i += 1
            x = ""
            while i < len(lexer_result) and lexer_result[i].value != ";":
                x += f"{lexer_result[i].value} "
                i += 1
            assembly_code += code_generator.generate_code(":=", token_value, x.strip())
    else:
        i += 1


print("\n...\nGenerated Assembly Code:\n...")
print(assembly_code)
