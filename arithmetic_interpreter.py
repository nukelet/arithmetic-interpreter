INTEGER = 'INTEGER'
PLUS, MINUS, TIMES, DIVIDE = 'PLUS', 'MINUS', 'TIMES', 'DIVIDE' 
EOF = 'EOF'
OPERATOR = 'OPERATOR'
operations = {
    '+' : PLUS,
    '-' : MINUS,
    '*' : TIMES,
    '/' : DIVIDE
}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        
        self.current_char = None
        if len(text) > 0:
            self.current_char = self.text[0]

        self.tokens = []

    def advance(self):
        self.pos += 1
        if (self.pos > len(self.text) - 1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def read_int(self):
        n = ''
        while self.current_char is not None and self.current_char.isdigit():
            n += self.current_char
            self.advance()
    
        return int(n)

    # def read_str(self):
    #     s = ''
    #     while self.current_char is not None and not (self.current_char.isspace()):
    #         s += self.current_char
    #         self.advance()
    #     return s

    def get_tokens(self):
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespaces()

            if self.current_char.isdigit():
                self.tokens.append(Token(INTEGER, self.read_int()))

            else:
                # self.tokens.append(Token(OPERATOR, self.read_str()))
                self.tokens.append(Token(OPERATOR, self.current_char))
                self.advance()

        self.tokens.append(Token(EOF, 'EOF'))
        return self.tokens


class Evaluator:
    # all operators currently receive two tokens
    def PLUS(self, a, b):
        if a is None or b is None:
            raise Exception("Parsing error: invalid syntax")
        if a.type is not INTEGER or b.type is not INTEGER:
            raise Exception("Parsing error: invalid syntax")
        return Token(INTEGER, a.value + b.value)

    def MINUS(self, a, b):
        if a.type is not INTEGER or b.type is not INTEGER:
            raise Exception("Parsing error: invalid syntax")
        return Token(INTEGER, a.value - b.value)

    def TIMES(self, a, b):
        if a.type is not INTEGER or b.type is not INTEGER:
            raise Exception("Parsing error: invalid syntax")
        return Token(INTEGER, a.value * b.value)
    
    def DIVIDE(self, a, b):
        if a.type is not INTEGER or b.type is not INTEGER:
            raise Exception("Parsing error: invalid syntax")
        return Token(INTEGER, int(a.value / b.value))

    def __init__(self):
        self.operations = {
            '+' : self.PLUS,
            '-' : self.MINUS,
            '*' : self.TIMES,
            '/' : self.DIVIDE
        }

    def error(self, token):
        raise Exception(f"Invalid operator: {token.value}")

    def evaluate(self, operation, a, b):
        if operation.value not in self.operations:
            self.error(operation)
        else:
            return self.operations[operation.value](a, b)

# simple interpreter that implements a single grammar rule:
# (INTEGER) (OPERATOR) (INTEGER)
class Interpreter:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.evaluator = Evaluator()

        self.tokens = self.lexer.get_tokens()
        self.pos = 0
        
        if len(self.tokens) > 0:
            self.current_token = self.tokens[0]
        
        else:
            self.current_token = None

    def error(self):
        raise Exception("Error parsing expression!")
    
    def eat(self, type):
        if self.current_token.type == type:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token

    def evaluate(self, operation, a, b):
        return self.evaluator.evaluate(operation, a, b)

    def expr(self):
        result = self.term()

        if self.current_token.type != OPERATOR:
            self.error()

        while self.current_token.type == OPERATOR:
            operation = self.current_token
            self.eat(OPERATOR)
            next_token = self.current_token

            result = self.evaluate(operation, result, next_token)
            self.eat(INTEGER)

        if result is None:
            return None

        else:
            return result.value

def main():
    while True:
        text = input("> ")
        interpreter = Interpreter(text)

        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()