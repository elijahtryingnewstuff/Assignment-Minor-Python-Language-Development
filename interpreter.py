from nodes import *
from values import Number, Boolean, String

class Interpreter:
    def __init__(self):
        self.visit_map = {
            NumberNode: self.visit_number,  
            BooleanNode: self.visit_boolean,
            StringNode: self.visit_string,  
            AddNode: self.visit_add,
            SubtractNode: self.visit_subtract,
            MultiplyNode: self.visit_multiply,
            DivideNode: self.visit_divide,
            EqualsNode: self.visit_equals,
            NotEqualsNode: self.visit_not_equals,
            LessThanNode: self.visit_less_than,
            GreaterThanNode: self.visit_greater_than,
            LessThanOrEqualNode: self.visit_less_than_or_equal,
            GreaterThanOrEqualNode: self.visit_greater_than_or_equal,
            AndNode: self.visit_and,
            OrNode: self.visit_or,
            NotNode: self.visit_not,
            PowerNode: self.visit_power,
        }


    def visit_number(self, node):
        """Evaluate the number node."""
        return Number(node.value)

    def visit_boolean(self, node):
        """Evaluate the boolean node."""
        return Boolean(node.value)

    def visit_string(self, node):
        """Evaluate the string node."""
        return String(node.value)

    def visit_add(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)

        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on boolean and numeric types.")

        if isinstance(left, String) and isinstance(right, String):
            return String(left.value + right.value)

        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)
        raise TypeError("Unsupported operands for addition")
    

    def visit_subtract(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)

        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on boolean and numeric types.")
        
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value - right.value)
        raise TypeError("Unsupported operands for subtraction")

    def visit_multiply(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)

        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on boolean and numeric types.")
        
        if isinstance(left, String) and isinstance(right, Number):
            return String(left.value * int(right.value))
        
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)
        raise TypeError("Unsupported operands for multiplication")
    

    def visit_divide(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on boolean and numeric types.")
        if right.value == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value / right.value)
        raise TypeError("Unsupported operands for division")


    def visit_equals(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if type(left) != type(right):
            return Boolean(False) 
        return Boolean(left.value == right.value)


    def visit_not_equals(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if type(left) != type(right):
            return Boolean(True)  
        return Boolean(left.value != right.value)


    def visit_less_than(self, node):
        return Boolean(self.evaluate(node.node_a).value < self.evaluate(node.node_b).value)

    def visit_greater_than(self, node):
        return Boolean(self.evaluate(node.node_a).value > self.evaluate(node.node_b).value)

    def visit_less_than_or_equal(self, node):
        return Boolean(self.evaluate(node.node_a).value <= self.evaluate(node.node_b).value)

    def visit_greater_than_or_equal(self, node):
        return Boolean(self.evaluate(node.node_a).value >= self.evaluate(node.node_b).value)

    def visit_and(self, node):
        return Boolean(self.evaluate(node.node_a).value and self.evaluate(node.node_b).value)

    def visit_or(self, node):
        return Boolean(self.evaluate(node.node_a).value or self.evaluate(node.node_b).value)

    def visit_not(self, node):
        return Boolean(not self.evaluate(node.node).value)

    def visit_power(self, node):
        return Number(self.evaluate(node.node_a).value ** self.evaluate(node.node_b).value)


    def evaluate(self, node):
        """Evaluate the AST."""
        node_type = type(node)
        if node_type in self.visit_map:
            return self.visit_map[node_type](node)
        else:
            raise RuntimeError(f"Unexpected node type: {node_type}")
