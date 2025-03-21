import re
from tokens import Token, TokenType

WHITESPACE = ' \n\t'
DIGITS = '0123456789'

MULTI_CHAR_TOKENS = {
    '==': TokenType.EQUALS,
    '!=': TokenType.NOTEQUAL,
    '<=': TokenType.LESSEQ,
    '>=': TokenType.GREATEREQ,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
}


class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.current_char = None
        self.advance()


    def advance(self):
        """Move to the next character."""
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None


    def generate_tokens(self):
        """Generate tokens from the input text."""
        while self.current_char is not None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char in DIGITS or self.current_char == '.':
                yield self.generate_number()
            elif self.current_char == '"':
                yield self.generate_string()
            elif self.current_char in ('+', '-', '*', '/', '(', ')', '<', '>', '!', '='):
                yield self.generate_operator_or_comparison()
            elif self.current_char in ('a', 'o', 't', 'f'):  
                yield self.generate_keyword()
            else:
                raise ValueError(f"Unexpected character: {self.current_char}")
            

    def generate_number(self):
        """Generate a number token."""
        number_str = self.current_char
        self.advance()

        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            number_str += self.current_char
            self.advance()
        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str += '0'
        return Token(TokenType.NUMBER, float(number_str))


    def generate_string(self):
        """Generate a string token."""
        self.advance()  
        string = ""
        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()
        if self.current_char != '"':
            raise ValueError("Unterminated string literal")
        self.advance() 
        return Token(TokenType.STRING, string)
    

    def generate_operator_or_comparison(self):
        """Generate tokens for operators or comparisons."""
        char = self.current_char
        self.advance()

        if char == '!' and self.current_char == '=':
            self.advance()
            return Token(TokenType.NOTEQUAL)
        elif char == '=' and self.current_char == '=':
            self.advance()
            return Token(TokenType.EQUALS)
        elif char == '<' and self.current_char == '=':
            self.advance()
            return Token(TokenType.LESSEQ)
        elif char == '>' and self.current_char == '=':
            self.advance()
            return Token(TokenType.GREATEREQ)
        elif char == '!':
            return Token(TokenType.NOT)
        elif char == '<':
            return Token(TokenType.LESS)
        elif char == '>':
            return Token(TokenType.GREATER)
        elif char == '+':
            return Token(TokenType.PLUS)
        elif char == '-':
            return Token(TokenType.MINUS)
        elif char == '*':
            return Token(TokenType.MULTIPLY)
        elif char == '/':
            return Token(TokenType.DIVIDE)
        elif char == '(':
            return Token(TokenType.LPAREN)
        elif char == ')':
            return Token(TokenType.RPAREN)
        else:
            raise ValueError(f"Unexpected operator: {char}")
        

    def generate_keyword(self):
        """Generate tokens for keywords like 'and', 'or', 'true', 'false'."""
        keyword = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char.isalpha():
            keyword += self.current_char
            self.advance()
        if keyword in MULTI_CHAR_TOKENS:
            return Token(MULTI_CHAR_TOKENS[keyword])
        else:
            raise ValueError(f"Unexpected keyword: {keyword}")