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
            if self.current_token.type == TokenType.SEMICOLON:
                self.advance()
                continue
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
        return statements

    def statement(self):
        if self.current_token is None:
            return None
        if self.current_token.type == TokenType.IF:
            return self.parse_if()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while()
        elif self.current_token.type == TokenType.BREAK:
            return self.parse_break()
        elif self.current_token.type == TokenType.PRINT:
            self.advance()
            expr = self.expr()
            return PrintNode(expr)
        elif self.current_token.type == TokenType.INPUT:
            return self.parse_input()
        elif self.current_token.type == TokenType.IDENTIFIER:
            identifier = self.current_token.value
            self.advance()
            if self.current_token and self.current_token.type == TokenType.ASSIGN:
                self.advance()
                if self.current_token and self.current_token.type == TokenType.INPUT:
                    input_node = self.parse_input()
                    return AssignNode(identifier, input_node)
                expr = self.expr()
                return AssignNode(identifier, expr)
            return IdentifierNode(identifier)
        return self.expr()

    def parse_if(self):
        self.advance()
        if not self.current_token or self.current_token.type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after 'if'")
        self.advance()
        condition = self.expr()
        if not self.current_token or self.current_token.type != TokenType.RPAREN:
            raise SyntaxError("Expected ')' after if condition")
        self.advance()
        true_block = self.parse_block()
        false_block = None
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self.advance()
            false_block = self.parse_block()
        return IfNode(condition, true_block, false_block)

    def parse_while(self):
        self.advance()
        if not self.current_token or self.current_token.type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after 'while'")
        self.advance()
        condition = self.expr()
        if not self.current_token or self.current_token.type != TokenType.RPAREN:
            raise SyntaxError("Expected ')' after while condition")
        self.advance()
        body = self.parse_block()
        return WhileNode(condition, body)

    def parse_break(self):
        self.advance()
        return BreakNode()

    def parse_input(self):
        self.advance()
        if not self.current_token or self.current_token.type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after 'input'")
        self.advance()
        prompt = self.expr()
        if not self.current_token or self.current_token.type != TokenType.RPAREN:
            raise SyntaxError("Expected ')' after input prompt")
        self.advance()
        return InputNode(prompt)

    def parse_block(self):
        if not self.current_token or self.current_token.type != TokenType.LBRACE:
            raise SyntaxError("Expected '{' to start a block")
        self.advance()
        statements = []
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
        if not self.current_token or self.current_token.type != TokenType.RBRACE:
            raise SyntaxError("Expected '}' to end a block")
        self.advance()
        return statements

    def expr(self):  # Lowest precedence: + and -
        result = self.logic_or()
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.type
            self.advance()
            right = self.logic_or()
            if operator == TokenType.PLUS:
                result = AddNode(result, right)
            else:
                result = SubtractNode(result, right)
        return result

    def logic_or(self):  # Middle-low precedence: or
        result = self.logic_and()
        while self.current_token and self.current_token.type == TokenType.OR:
            self.advance()
            right = self.logic_and()
            result = OrNode(result, right)
        return result

    def logic_and(self):  # Middle-high precedence: and
        result = self.comp()
        while self.current_token and self.current_token.type == TokenType.AND:
            self.advance()
            right = self.comp()
            result = AndNode(result, right)
        return result

    def comp(self):  # Higher precedence: comparisons
        result = self.term()
        while self.current_token and self.current_token.type in (
            TokenType.EQUALS, TokenType.NOTEQUAL, TokenType.LESS, TokenType.GREATER,
            TokenType.LESSEQ, TokenType.GREATEREQ
        ):
            operator = self.current_token.type
            self.advance()
            right = self.term()
            result = self.create_binary_node(operator, result, right)
        return result

    def term(self):
        result = self.factor()
        while self.current_token and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.current_token.type
            self.advance()
            right = self.factor()
            if operator == TokenType.MULTIPLY:
                result = MultiplyNode(result, right)
            elif operator == TokenType.DIVIDE:
                result = DivideNode(result, right)
            elif operator == TokenType.MODULO:
                result = ModuloNode(result, right)
        return result

    def factor(self):
        token = self.current_token
        if not token:
            raise SyntaxError("Unexpected end of input")
        if token.type == TokenType.MINUS:
            self.advance()
            operand = self.factor()
            return SubtractNode(NumberNode(0), operand)
        elif token.type == TokenType.LPAREN:
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