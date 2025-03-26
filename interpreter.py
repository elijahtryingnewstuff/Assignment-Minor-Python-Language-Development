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
            IfNode: self.visit_if,
            WhileNode: self.visit_while,
            BreakNode: self.visit_break,
            InputNode: self.visit_input,
            ModuloNode: self.visit_modulo,
        }

    def visit_number(self, node):
        return Number(node.value)

    def visit_boolean(self, node):
        return Boolean(node.value)

    def visit_string(self, node):
        return String(node.value)

    def visit_add(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        # String concatenation
        if isinstance(left, String) or isinstance(right, String):
            left_val = str(int(left.value)) if isinstance(left, Number) and left.value.is_integer() else str(left.value)
            right_val = str(int(right.value)) if isinstance(right, Number) and right.value.is_integer() else str(right.value)
            return String(left_val + right_val)

        if isinstance(left, String) or isinstance(right, String):
            return String(str(left.value) + str(right.value))
        
        # Check for booleans first
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on booleans. Use logical operators (and/or) instead")
        
        # Rest of your existing add logic...
        if isinstance(left, String) and isinstance(right, String):
            return String(left.value + right.value)
            
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)
            
        raise TypeError(f"Cannot add {type(left).__name__} and {type(right).__name__}. Supported: Number+Number or String+String")

    def visit_subtract(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on booleans. Use logical operators (and/or) instead")
                
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value - right.value)
            
        raise TypeError(f"Cannot subtract {type(left).__name__} and {type(right).__name__}. Only numbers supported")

    def visit_multiply(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform arithmetic on booleans. Use logical operators (and/or) instead")
        
        # Add symmetric string multiplication
        if isinstance(left, String) and isinstance(right, Number):
            return String(left.value * int(right.value))
        if isinstance(left, Number) and isinstance(right, String):
            return String(right.value * int(left.value))
        
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)
            
        raise TypeError(f"Cannot multiply {type(left).__name__} and {type(right).__name__}")

    def visit_divide(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError(f"Invalid operation between {type(left).__name__} and {type(right).__name__}. Comparisons must be isolated, e.g., (2 + 3) == 5")
            
        if not (isinstance(left, Number) and isinstance(right, Number)):
            raise TypeError(f"Cannot divide {type(left).__name__} and {type(right).__name__}. Only numbers supported")
            
        if right.value == 0:
            raise ZeroDivisionError("Division by zero")
            
        return Number(left.value / right.value)

    def visit_modulo(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform modulo with boolean values")
            
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value % right.value)
            
        raise TypeError(f"Cannot perform modulo on {type(left).__name__} and {type(right).__name__}. Only numbers supported")

    def visit_power(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if isinstance(left, Boolean) or isinstance(right, Boolean):
            raise TypeError("Cannot perform exponentiation with boolean values")
            
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value ** right.value)
            
        raise TypeError(f"Cannot exponentiate {type(left).__name__} and {type(right).__name__}. Only numbers supported")

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
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if not (isinstance(left, Number) and isinstance(right, Number)):
            raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__} with <. Only numbers supported")
        return Boolean(left.value < right.value)

    def visit_greater_than(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if not (isinstance(left, Number) and isinstance(right, Number)):
            raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__} with >. Only numbers supported")
        return Boolean(left.value > right.value)

    def visit_less_than_or_equal(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if not (isinstance(left, Number) and isinstance(right, Number)):
            raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__} with <=. Only numbers supported")
        return Boolean(left.value <= right.value)

    def visit_greater_than_or_equal(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        # Special case: if one is string-number and other is number
        if isinstance(left, String) and right.isdigit():
            left = Number(float(left.value))
        elif isinstance(right, String) and right.isdigit():
            right = Number(float(right.value))
        
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value >= right.value)
        raise TypeError(...)

    def visit_and(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if not (isinstance(left, Boolean) and isinstance(right, Boolean)):
            raise TypeError(f"Cannot perform AND on {type(left).__name__} and {type(right).__name__}. Only booleans supported")
        return Boolean(left.value and right.value)

    def visit_or(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if not (isinstance(left, Boolean) and isinstance(right, Boolean)):
            raise TypeError(f"Cannot perform OR on {type(left).__name__} and {type(right).__name__}. Only booleans supported")
        return Boolean(left.value or right.value)

    def visit_not(self, node):
        value = self.evaluate(node.node)
        
        if not isinstance(value, Boolean):
            raise TypeError(f"Cannot perform NOT on {type(value).__name__}. Only boolean supported")
        return Boolean(not value.value)


    def visit_assign(self, node):
        value = self.evaluate(node.expression)
        self.globals[node.identifier] = value
        return value

    def visit_print(self, node):
        value = self.evaluate(node.expression)
        print(value)  
        return None 

    def visit_identifier(self, node):
        if node.identifier not in self.globals:
            raise NameError(f"Variable '{node.identifier}' is not defined")
        return self.globals[node.identifier]

    def visit_if(self, node):
        condition = self.evaluate(node.condition)
        if not isinstance(condition, Boolean):
            raise TypeError("If condition must be boolean")
        if condition.value:
            for stmt in node.true_block:
                self.evaluate(stmt)
        elif node.false_block:
            for stmt in node.false_block:
                self.evaluate(stmt)
        return None

    def visit_while(self, node):
        while True:
            condition = self.evaluate(node.condition)
            if not isinstance(condition, Boolean):
                raise TypeError("While condition must be boolean")
            if not condition.value:
                break
            try:
                for stmt in node.body:
                    self.evaluate(stmt)
            except BreakException:
                break
        return None

    def visit_break(self, node):
        raise BreakException()

    def visit_input(self, node):
        prompt = self.evaluate(node.prompt)
        if not isinstance(prompt, String):
            raise TypeError("Input prompt must be a string")
        user_input = input(prompt.value).strip()
        
        # Strict number detection
        try:
            if user_input.isdigit() or (user_input.replace('.','',1).isdigit() and user_input.count('.') < 2):
                return Number(float(user_input))
        except:
            pass
        return String(user_input)

    def evaluate(self, node):
        if node is None:
            return None
        if isinstance(node, list):
            result = None
            for stmt in node:
                result = self.evaluate(stmt)
            return result
        node_type = type(node)
        if node_type in self.visit_map:
            return self.visit_map[node_type](node)
        raise RuntimeError(f"Unexpected node type: {node_type}")

class BreakException(Exception):
    pass