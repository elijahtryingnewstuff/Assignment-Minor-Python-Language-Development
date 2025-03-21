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
            if self.current_token.type == TokenType.PRINT:
                self.advance()
                expression = self.expr()
                statements.append(PrintNode(expression))
                self.advance()  # Fix: Move to next token
            elif self.current_token.type == TokenType.IDENTIFIER:
                identifier = self.current_token.value
                self.advance()
                if self.current_token.type == TokenType.EQUALS:
                    self.advance()
                    expression = self.expr()
                    statements.append(AssignNode(identifier, expression))
                    self.advance()  # Fix: Move to next token
                else:
                    raise SyntaxError("Expected assignment operator '='")
            else:
                statements.append(self.expr())
                self.advance()  # Fix: Move to next token
        return statements

    def expr(self):
        result = self.comp()
        while self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.type
            self.advance()
            right = self.comp()
            if operator == TokenType.PLUS:
                result = AddNode(result, right)
            else:
                result = SubtractNode(result, right)
        return result

    def comp(self):
        result = self.term()
        while self.current_token is not None and self.current_token.type in (
            TokenType.EQUALS, TokenType.NOTEQUAL, TokenType.LESS, TokenType.GREATER, 
            TokenType.LESSEQ, TokenType.GREATEREQ
        ):
            operator = self.current_token.type
            self.advance()
            right = self.term()
            result = self.create_binary_node(operator, result, right)
        
        while self.current_token is not None and self.current_token.type in (TokenType.AND, TokenType.OR):
            operator = self.current_token.type
            self.advance()
            right = self.comp()  # Recursively parse AND/OR expressions
            if operator == TokenType.AND:
                result = AndNode(result, right)
            else:
                result = OrNode(result, right)

        return result



    def term(self):
        result = self.factor()
        while self.current_token is not None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token.type
            self.advance()
            right = self.factor()
            if operator == TokenType.MULTIPLY:
                result = MultiplyNode(result, right)
            else:
                result = DivideNode(result, right)
        return result


    def factor(self):
        token = self.current_token
        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()
            if self.current_token.type != TokenType.RPAREN:
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
        elif token.type == TokenType.NOT:  # Fix: Handle NOT
            self.advance()
            return NotNode(self.factor())  
        else:
            raise SyntaxError(f"Unexpected token: {token}")


    def create_binary_node(self, operator, left, right):
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