from tokens import TokenType, Token
from nodes import *
from values import List
from typing import Optional

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token: Optional[Token] = None
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

  
    def expect(self, token_type):
        if not self.current_token or self.current_token.type != token_type:
            raise SyntaxError(f"Expected token {token_type}, got {self.current_token}")
        self.advance()

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
        elif self.current_token.type == TokenType.FUNCTION:
            return self.parse_function()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return()
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
            return self.parse_assignment_or_identifier()
        return self.expr()

    # In Parser class
    def parse_assignment_or_identifier(self):
        name = self.current_token.value  # get the identifier name
        self.advance()
        # If identifier is followed by '(', parse a function call
        if self.current_token and self.current_token.type == TokenType.LPAREN:
            return self.parse_call(name)
        # Handle possible indexing after the identifier (e.g., d[...]...)
        node = IdentifierNode(name)
        node = self.handle_possible_indexing(node)  # builds IndexNode chains for any [] following the identifier
        # If an assignment '=' follows, create the appropriate assignment node
        if self.current_token and self.current_token.type == TokenType.ASSIGN:
            self.advance()
            value_expr = self.expr()
            if isinstance(node, IdentifierNode):
                # Simple variable assignment (no indexing)
                return AssignNode(name, value_expr)
            else:
                # Assignment to an indexed element (dictionary or list)
                # node is an IndexNode with node.container as the target structure and node.index_expr as the key/index
                return DictAssignNode(node.container, node.index_expr, value_expr)
        # If no assignment, return the identifier or indexed-access node
        return node


    def parse_call(self, name):
        self.advance()  # Skip '('
        arguments = []
        while self.current_token and self.current_token.type != TokenType.RPAREN:
            arguments.append(self.expr())
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
        if not self.current_token or self.current_token.type != TokenType.RPAREN:
            raise SyntaxError("Expected ')' after function arguments")
        self.advance()  # Skip ')'
        return CallNode(name, arguments)

    def parse_if(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.expr()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)

        body = []
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        self.expect(TokenType.RBRACE)

        else_body = None
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.LBRACE)
            else_body = []
            while self.current_token and self.current_token.type != TokenType.RBRACE:
                else_body.append(self.statement())
            self.expect(TokenType.RBRACE)

        return IfNode(condition, body, else_body)


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

    def parse_list(self):
        self.advance()  # Skip '['
        elements = []
        while self.current_token and self.current_token.type != TokenType.RBRACKET:
            elements.append(self.expr())
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
        if not self.current_token or self.current_token.type != TokenType.RBRACKET:
            raise SyntaxError("Expected ']' after list")
        self.advance()
        list_node = ListNode(elements)
        return self.handle_possible_indexing(list_node)

    def handle_possible_indexing(self, node):
        while self.current_token and self.current_token.type == TokenType.LBRACKET:
            self.advance()  # Skip '['
            key = self.expr()  # Parse full expression inside brackets
            if not self.current_token or self.current_token.type != TokenType.RBRACKET:
                raise SyntaxError("Expected ']' after index")
            self.advance()  # Skip ']'
            node = IndexNode(node, key)  # Always use IndexNode, let interpreter decide type
        return node
        

    def expr(self):
        return self.logic_or()


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
        while self.current_token and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.current_token.type
            self.advance()
            right = self.factor()
            if op == TokenType.MULTIPLY:
                left = MultiplyNode(left, right)
            elif op == TokenType.DIVIDE:
                left = DivideNode(left, right)
            else:  # MODULO
                left = ModuloNode(left, right)
        return left


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
            TokenType.EQUALS, TokenType.NOTEQUAL,
            TokenType.LESS, TokenType.GREATER,
            TokenType.LESSEQ, TokenType.GREATEREQ,
            TokenType.IS  # Add this
        ):
            op = self.current_token.type
            self.advance()
            right = self.add_sub()
            left = self.create_binary_node(op, left, right)
        return left

    def term(self):
        result = self.factor()
        while self.current_token and self.current_token.type in (
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO
        ):
            operator = self.current_token.type
            self.advance()
            right = self.factor()
            if operator == TokenType.PLUS:
                result = AddNode(result, right)
            elif operator == TokenType.MINUS:
                result = SubtractNode(result, right)
            elif operator == TokenType.MULTIPLY:
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
        
        if token.type == TokenType.LPAREN:
            self.advance()  # Skip '('
            expr = self.expr()
            if not self.current_token or self.current_token.type != TokenType.RPAREN:
                raise SyntaxError("Expected ')'")
            self.advance()  # Skip ')'
            left = expr

        elif token.type == TokenType.LBRACKET:
            left = self.parse_list()

        elif token.type == TokenType.NUMBER:
            self.advance()
            left = NumberNode(token.value)

        elif token.type == TokenType.IDENTIFIER:
            left = self.parse_assignment_or_identifier()

        elif token.type == TokenType.TRUE:
            self.advance()
            left = BooleanNode(True)

        elif token.type == TokenType.FALSE:
            self.advance()
            left = BooleanNode(False)

        elif token.type == TokenType.LBRACE:
            dict_node = self.parse_dict()
            left = self.handle_possible_indexing(dict_node)

        elif token.type == TokenType.STRING:
            self.advance()
            left = StringNode(token.value)

        elif token.type == TokenType.NOT:
            self.advance()
            return NotNode(self.factor())

        elif token.type == TokenType.INPUT:
            return self.parse_input()

        else:
            raise SyntaxError(f"Unexpected token: {token}")

        # Handle exponentiation (right-associative): e.g., 2 ** 3 ** 2 → 2 ** (3 ** 2)
        while self.current_token and self.current_token.type == TokenType.POW:
            self.advance()
            right = self.factor()
            left = PowerNode(left, right)

        return left

        

    def parse_dict(self):
        self.advance()  # Skip '{'
        elements = {}
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            # Key must be a literal value (string, number, boolean)
            if self.current_token.type not in (TokenType.STRING, TokenType.NUMBER, TokenType.TRUE, TokenType.FALSE):
                raise SyntaxError("Dictionary keys must be strings, numbers, or booleans")
            
            key_node = self.factor()  # This creates the appropriate node type
            
            # Convert key_node to a hashable Python type
            if isinstance(key_node, StringNode):
                key = key_node.value
            elif isinstance(key_node, NumberNode):
                key = key_node.value
            elif isinstance(key_node, BooleanNode):
                key = key_node.value
            else:
                raise SyntaxError("Dictionary keys must be strings, numbers, or booleans")
            
            if not self.current_token or self.current_token.type != TokenType.COLON:
                raise SyntaxError("Expected ':' after dictionary key")
            self.advance()  # Skip ':'
            
            value_node = self.expr()  # Value can be any expression
            elements[key] = value_node
            
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()  # Skip ','
        
        if not self.current_token or self.current_token.type != TokenType.RBRACE:
            raise SyntaxError("Expected '}' after dictionary")
        self.advance()  # Skip '}'
        return DictNode(elements)
    

    def parse_function(self):
        self.advance()  # Skip 'def' or 'function'
        
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function name")
        
        name = self.current_token.value
        self.advance()
        
        if not self.current_token or self.current_token.type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after function name")
        self.advance()
        
        parameters = []
        while self.current_token and self.current_token.type != TokenType.RPAREN:
            if self.current_token.type != TokenType.IDENTIFIER:
                raise SyntaxError("Expected parameter name")
            parameters.append(self.current_token.value)
            self.advance()
            
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
        
        if not self.current_token or self.current_token.type != TokenType.RPAREN:
            raise SyntaxError("Expected ')' after parameters")
        self.advance()
        
        if not self.current_token or self.current_token.type != TokenType.LBRACE:
            raise SyntaxError("Expected '{' to start function body")
        
        body = self.parse_block()
        
        return FunctionNode(name, parameters, body)


    def parse_return(self):
        self.advance()  # Skip 'return'
        if self.current_token and self.current_token.type not in (TokenType.SEMICOLON, TokenType.RBRACE):
            value = self.expr()
        else:
            value = None
        return ReturnNode(value)

    def handle_possible_indexing(self, node):
        while self.current_token and self.current_token.type == TokenType.LBRACKET:
            self.advance()  # Skip '['
            key = self.expr()  # Parse full expression inside brackets
            if not self.current_token or self.current_token.type != TokenType.RBRACKET:
                raise SyntaxError("Expected ']' after index")
            self.advance()  # Skip ']'
            node = IndexNode(node, key)  # Always use IndexNode
        return node
    
    def create_binary_node(self, operator, left, right):
        operator_map = {
            TokenType.EQUALS: EqualsNode,
            TokenType.NOTEQUAL: NotEqualsNode,
            TokenType.LESS: LessThanNode,
            TokenType.GREATER: GreaterThanNode,
            TokenType.LESSEQ: LessThanOrEqualNode,
            TokenType.GREATEREQ: GreaterThanOrEqualNode,
            TokenType.IS: IsNode,
        }
        return operator_map[operator](left, right)