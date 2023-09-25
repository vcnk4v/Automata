# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"


# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD,
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == "_"):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == "_"):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char == "_")

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(
                source_code[position]
            ):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == ".":
                    if position + 1 < len(source_code):
                        next_next_char = source_code[position + 1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(
                        source_code[position]
                    ):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(
                            f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits"
                        )

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens


########################## BOILERPLATE ENDS ###########################
def if_function(tokens):
    global index
    brackets = 0
    if index < len(tokens):
        if tokens[index][1] != "(":
            raise SyntaxError("No brackets provided for if condition")

        condition_function(tokens)
        if index >= len(tokens):
            raise SyntaxError("No statement provided for if")

        statement_function(tokens)

        if index < len(tokens):
            if tokens[index][1] == "(":
                index += 1
                brackets += 1

        if (
            index < len(tokens)
            and tokens[index][0] == "KEYWORD"
            and tokens[index][1] == "else"
        ):
            index += 1
            if index < len(tokens):
                if tokens[index][1] == ")":
                    index += 1
                    brackets -= 1
            statement_function(tokens)
    if brackets != 0:
        raise SyntaxError("Wrong brackets")


def y_function(tokens):
    global index
    while index < len(tokens):
        if (
            tokens[index][0] == "INTEGER"
            or tokens[index][0] == "FLOAT"
            or tokens[index][0] == "IDENTIFIER"
            or tokens[index][0] == "KEYWORD"
            or tokens[index][1] == ";"
        ) and (tokens[index][1] != "else" and tokens[index][1] != "if"):
            index += 1
        elif tokens[index][1] == "-" or tokens[index][1] == "+":
            if ( index!=0 and
                tokens[index - 1][0] == "INTEGER"
                or tokens[index - 1][0] == "FLOAT"
                or tokens[index - 1][0] == "IDENTIFIER"
            ):
                raise SyntaxError("Expression doesnt belong to statement alphabet")
            else:
                index += 1
        else:
            break


def condition_function(tokens):
    global index
    brackets = 0
    if index < len(tokens):
        if tokens[index][1] == "(":
            index += 1
            brackets += 1
            x_function(tokens)
            if tokens[index][1] == ")":
                index += 1
                brackets -= 1
                return

            op_function(tokens)
            x_function(tokens)
            if tokens[index][1] == ")":
                index += 1
                brackets -= 1
            else:
                raise SyntaxError("Wrong syntax for operations")
        else:
            x_function(tokens)
    if brackets != 0:
        raise SyntaxError("Error in if condition")


def x_function(tokens):
    global index
    brackets = 0
    if index < len(tokens):
        if tokens[index][0] == "INTEGER" or tokens[index][0] == "FLOAT":
            index += 1
        elif tokens[index][1] == "(":
            index += 1
            brackets += 1
            x_function(tokens)
            op_function(tokens)
            x_function(tokens)
            if tokens[index][1] == ")":
                index += 1
                brackets -= 1
        else:
            y_function(tokens)
    if brackets != 0:
        raise SyntaxError("Wrong brackers in condition expression")


def op_function(tokens):
    global index
    opns = ["+", "-", "*", "/", "^", ">", "<", "="]
    if index < len(tokens):
        if tokens[index][0] == "SYMBOL" and tokens[index][1] in opns:
            index += 1
        else:
            raise SyntaxError(f"Wrong operand: {tokens[index][1]}")
    else:
        raise SyntaxError("Expression cannot end with operand")


def statement_function(tokens):
    global index
    global s_brackets
    s_brackets = 0
    if index >= len(tokens):
        return
    if tokens[index][1] == "if":
        index += 1
        if_function(tokens)
    if index < len(tokens) and tokens[index][1] == "else":
        raise SyntaxError("else occurs before if")

    if index < len(tokens) and tokens[index][0] == "SYMBOL" and tokens[index][1] == "(":
        index += 1
        s_brackets += 1
        statement_function(tokens)
        if index < len(tokens) and tokens[index][1] == ")":
            s_brackets -= 1
            index += 1
            statement_function(tokens)
    elif index < len(tokens):
        y_function(tokens)
    if s_brackets != 0:
        raise SyntaxError("Wrong brackets in statement")


def checkGrammar(tokens):
    global index
    index = 0
    statement_function(tokens)
    if index == len(tokens):
        return True
    else:
        raise SyntaxError("Invalid expression")

    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed


# Test the tokenizer
if __name__ == "__main__":
    source_code = "if (2+xi > 0) print 2.0 else print -1;"
    index = 0

    brackets = 0
    source_code = input()
    tokens = tokenize(source_code)

    logs = checkGrammar(
        tokens
    )  # You are tasked with implementing the function checkGrammar

    for token in tokens:
        print(f"Token Type: {token[0]}, Token Value: {token[1]}")

    print(logs)
