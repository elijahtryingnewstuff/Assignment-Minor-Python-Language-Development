from tokens import TokenType
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.advance()

    def advance(self):
        """Move to the next token."""
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None


    def parse(self):
        """Parse the tokens into an AST."""
        if self.current_token is None:
            return None
        result = self.expr()
        if self.current_token is not None:
            raise SyntaxError("Unexpected token at the end")
        return result


    def expr(self):
        """Handle logical expressions (and, or)."""
        result = self.comp()
        while self.current_token is not None and self.current_token.type in (TokenType.AND, TokenType.OR):
            operator = self.current_token.type
            self.advance()
            result = AndNode(result, self.comp()) if operator == TokenType.AND else OrNode(result, self.comp())
        return result


    def comp(self):
        """Handle comparisons (==, !=, <, >, <=, >=)."""
        result = self.term()
        while self.current_token is not None and self.current_token.type in (
            TokenType.EQUALS, TokenType.NOTEQUAL, TokenType.LESS, TokenType.GREATER, TokenType.LESSEQ, TokenType.GREATEREQ
        ):
            operator = self.current_token.type
            self.advance()
            result = self.create_binary_node(operator, result, self.term())
        return result


    def term(self):
        """Handle addition and subtraction."""
        result = self.factor()
        while self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.type
            self.advance()
            result = self.create_binary_node(operator, result, self.factor())
        return result


    def factor(self):
        """Handle multiplication, division, and unary operations."""
        result = self.power()
        while self.current_token is not None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token.type
            self.advance()
            result = self.create_binary_node(operator, result, self.power())
        return result
    

    def power(self):
        """Handle exponentiation."""
        result = self.unary()
        while self.current_token is not None and self.current_token.type == TokenType.POW:
            self.advance()
            result = PowerNode(result, self.unary())
        return result
    

    def unary(self):
        """Handle unary operations (+, -, !)."""
        if self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.NOT):
            operator = self.current_token.type
            self.advance()
            if operator == TokenType.NOT:
                return NotNode(self.unary())
            elif operator == TokenType.MINUS:
                return SubtractNode(NumberNode(0), self.unary())
            else:
                return self.unary()  
        return self.atom()
    

    def atom(self):
        token = self.current_token

        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()
            if self.current_token is None or self.current_token.type != TokenType.RPAREN:
                raise SyntaxError("Expected closing parenthesis ')'")
            self.advance()
            return result

        elif token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)

        elif token.type == TokenType.TRUE:
            self.advance()
            return BooleanNode(True)

        elif token.type == TokenType.FALSE:
            self.advance()
            return BooleanNode(False)
        
        elif token.type == TokenType.STRING: 
            self.advance()
            return StringNode(token.value)
        raise SyntaxError(f"Unexpected token: {token}")
    

    def create_binary_node(self, operator, left, right):
        """Create a binary node based on the operator."""
        operator_to_node = {
            TokenType.PLUS: AddNode,
            TokenType.MINUS: SubtractNode,
            TokenType.MULTIPLY: MultiplyNode,
            TokenType.DIVIDE: DivideNode,
            TokenType.EQUALS: EqualsNode,
            TokenType.NOTEQUAL: NotEqualsNode,
            TokenType.LESS: LessThanNode,
            TokenType.GREATER: GreaterThanNode,
            TokenType.LESSEQ: LessThanOrEqualNode,
            TokenType.GREATEREQ: GreaterThanOrEqualNode,
        }
        return operator_to_node[operator](left, right)