from nodes import *
from values import Number, Boolean, String

class Interpreter:
    def __init__(self):
        self.globals = {}  
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
            AssignNode: self.visit_assign,
            PrintNode: self.visit_print,
            IdentifierNode: self.visit_identifier,
        }

    def visit_assign(self, node):
        value = self.evaluate(node.expression)
        self.globals[node.identifier] = value
        print(f"Assigned {node.identifier} = {value}")
        return value

    def visit_print(self, node):
        value = self.evaluate(node.expression)
        print(value)
        return value

    def visit_identifier(self, node):
        if node.identifier in self.globals:
            return self.globals[node.identifier]
        raise NameError(f"Variable '{node.identifier}' is not defined")

    def visit_number(self, node):
        return Number(node.value)

    def visit_boolean(self, node):
        return Boolean(node.value)

    def visit_string(self, node):
        return String(node.value)

    def visit_add(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, String) and isinstance(right, String):
            return String(left.value + right.value)
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)
        raise TypeError(f"Cannot add {type(left).__name__} and {type(right).__name__}")


    def visit_subtract(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on boolean and numeric types.")
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value - right.value)
        raise TypeError(f"Cannot subtract {type(left)} and {type(right)}")


    def visit_multiply(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on boolean and numeric types.")
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)
        raise TypeError(f"Cannot multiply {type(left)} and {type(right)}")


    def visit_divide(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on boolean and numeric types.")
        if right.value == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value / right.value)
        raise TypeError(f"Cannot divide {type(left)} and {type(right)}")


    def visit_equals(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)

        if type(left) != type(right):
            return Boolean(False)
        if isinstance(left, String) and isinstance(right, String):
            return Boolean(left.value == right.value)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value == right.value)
        if isinstance(left, Boolean) and isinstance(right, Boolean):
            return Boolean(left.value == right.value)
        raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__}")


    def visit_not_equals(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if type(left) != type(right):
            return Boolean(True)
        if isinstance(left, String) and isinstance(right, String):
            return Boolean(left.value != right.value)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value != right.value)
        if isinstance(left, Boolean) and isinstance(right, Boolean):
            return Boolean(left.value != right.value)

        raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__}")

    def visit_less_than(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value < right.value) 
        if isinstance(left, String) and isinstance(right, String):
            return Boolean(left.value < right.value)
        raise TypeError(f"Cannot compare {type(left)} and {type(right)} with <")


    def visit_greater_than(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value > right.value)  
        if isinstance(left, String) and isinstance(right, String):
            return Boolean(left.value > right.value)
        raise TypeError(f"Cannot compare {type(left)} and {type(right)} with >")


    def visit_less_than_or_equal(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value <= right.value)  
        if isinstance(left, String) and isinstance(right, String):
            return Boolean(left.value <= right.value)
        raise TypeError(f"Cannot compare {type(left)} and {type(right)} with <=")


    def visit_greater_than_or_equal(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value >= right.value)  
        if isinstance(left, String) and isinstance(right, String):
            return Boolean(left.value >= right.value)
        raise TypeError(f"Cannot compare {type(left)} and {type(right)} with >=")


    def visit_and(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Boolean) and isinstance(right, Boolean):
            return Boolean(left.value and right.value)
        raise TypeError(f"Cannot perform logical AND on {type(left)} and {type(right)}")


    def visit_or(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Boolean) and isinstance(right, Boolean):
            return Boolean(left.value or right.value)
        raise TypeError(f"Cannot perform logical OR on {type(left)} and {type(right)}")


    def visit_not(self, node):
        value = self.evaluate(node.node)
        if isinstance(value, Boolean):
            return Boolean(not value.value)
        raise TypeError(f"Cannot perform logical NOT on {type(value)}")


    def visit_power(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value ** right.value)
        raise TypeError(f"Cannot perform exponentiation on {type(left)} and {type(right)}")


    def evaluate(self, node):
        node_type = type(node)
        if node_type in self.visit_map:
            return self.visit_map[node_type](node)
        else:
            raise RuntimeError(f"Unexpected node type: {node_type}")