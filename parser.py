from tokens import TokenType
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        statements = []
        while self.current_token is not None:
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def statement(self):
        if self.current_token.type == TokenType.PRINT:
            self.advance()
            expr = self.expr()
            return PrintNode(expr)
        elif self.current_token.type == TokenType.IDENTIFIER:
            identifier = self.current_token.value
            self.advance()
            if self.current_token and self.current_token.type == TokenType.EQUALS: 
                self.advance()
                expr = self.expr()
                return AssignNode(identifier, expr)
            else:
                return IdentifierNode(identifier)
        else:
            return self.expr()

    def expr(self):
        return self.logic_or()

    def logic_or(self):
        result = self.logic_and()
        while self.current_token and self.current_token.type == TokenType.OR:
            self.advance()
            right = self.logic_and()
            result = OrNode(result, right)
        return result

    def logic_and(self):
        result = self.comp()
        while self.current_token and self.current_token.type == TokenType.AND:
            self.advance()
            right = self.comp()
            result = AndNode(result, right)
        return result

    def comp(self):
        left = self.add_sub()
        while self.current_token and self.current_token.type in (
            TokenType.EQUALS, TokenType.NOTEQUAL, TokenType.LESS, TokenType.GREATER,
            TokenType.LESSEQ, TokenType.GREATEREQ
        ):
            op = self.current_token.type
            self.advance()
            right = self.add_sub()
            left = self.create_binary_node(op, left, right)
        return left

    def add_sub(self):
        left = self.mul_div()
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.type
            self.advance()
            right = self.mul_div()
            left = AddNode(left, right) if op == TokenType.PLUS else SubtractNode(left, right)
        return left

    def mul_div(self):
        left = self.factor()
        while self.current_token and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.current_token.type
            self.advance()
            right = self.factor()
            left = MultiplyNode(left, right) if op == TokenType.MULTIPLY else DivideNode(left, right)
        return left

    def factor(self):
        token = self.current_token
        if not token:
            raise SyntaxError("Unexpected end of input")
        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()
            if not self.current_token or self.current_token.type != TokenType.RPAREN:
                raise SyntaxError("Expected ')'")
            self.advance()
            return result
        elif token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return IdentifierNode(token.value)
        elif token.type == TokenType.TRUE:
            self.advance()
            return BooleanNode(True)
        elif token.type == TokenType.FALSE:
            self.advance()
            return BooleanNode(False)
        elif token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)
        elif token.type == TokenType.NOT:
            self.advance()
            return NotNode(self.factor())
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def create_binary_node(self, operator, left, right):
        operator_to_node = {
            TokenType.EQUALS: EqualsNode,
            TokenType.NOTEQUAL: NotEqualsNode,
            TokenType.LESS: LessThanNode,
            TokenType.GREATER: GreaterThanNode,
            TokenType.LESSEQ: LessThanOrEqualNode,
            TokenType.GREATEREQ: GreaterThanOrEqualNode,
        }
        return operator_to_node[operator](left, right)