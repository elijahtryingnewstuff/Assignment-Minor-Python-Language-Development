from nodes import *
from values import List, Dict, Number, Boolean, String
from typing import Dict as TypeDict, Type, Any, Callable
from values import ReturnValue, BreakSignal, ContinueSignal

class Interpreter:
    def __init__(self):
        self.globals = {}
        self.functions = {
            "to_string": {
                "parameters": ["value"],
                "body": [ReturnNode(None)]  # Placeholder; we'll handle it in visit_call
            }
        }
        self.scopes = [self.globals]
        self.in_function = False
        self.visit_map = {
            NumberNode: self.visit_number,
            BooleanNode: self.visit_boolean,
            StringNode: self.visit_string,
            ListNode: self.visit_list,
            DictNode: self.visit_dict,
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
            IndexNode: self.visit_index,
            DictAssignNode: self.visit_dict_assign,
            FunctionNode: self.visit_function,
            CallNode: self.visit_call,
            ReturnNode: self.visit_return,
            IsNode: self.visit_is,
            ToStringNode: self.visit_to_string,
            ListAssignNode: self.visit_index_assign,
            DictAccessNode: self.visit_dict_access,
        }

    
    def visit_number(self, node):
        return Number(node.value)

    def visit_boolean(self, node):
        return Boolean(node.value)

    def visit_string(self, node):
        return String(node.value)

    def visit_index_assign(self, node):
        container = self.evaluate(node.list_identifier)
        index = self.evaluate(node.index_expr)

        if isinstance(container, List):
            if not isinstance(index, Number):
                raise Exception("List index must be a number")
            idx = int(index.value)
            try:
                return container.elements[idx]
            except IndexError:
                raise Exception("List index out of range")

        elif isinstance(container, Dict):
            if isinstance(index, (String, Number, Boolean)):
                key = index.value
            else:
                raise Exception("Dictionary key must be string, number, or boolean")
            if key in container.elements:
                return container.elements[key]
            else:
                raise Exception(f"\"Key '{key}' not found in dictionary\"")

        else:
            raise Exception(f"Expected dictionary or list, got {type(container).__name__}")



    def visit_dict(self, node):
        evaluated_dict = {}
        for key, value_node in node.elements.items():
            evaluated_dict[key] = self.evaluate(value_node)
        return Dict(evaluated_dict)

    def visit_add(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)

        if isinstance(left, Dict) and isinstance(right, Dict):
            combined = {**left.elements, **right.elements}
            return Dict(combined)

        if isinstance(left, List) and isinstance(right, List):
            return List(left.elements + right.elements)

        if isinstance(left, String) and isinstance(right, String):
            return String(left.value + right.value)

        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)

        raise TypeError(f"Cannot add {type(left).__name__} and {type(right).__name__}")

    def visit_subtract(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value - right.value)
        raise TypeError(f"Cannot subtract {type(left).__name__} and {type(right).__name__}")

    def visit_multiply(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)
        raise TypeError(f"Cannot multiply {type(left).__name__} and {type(right).__name__}")

    def visit_divide(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if not (isinstance(left, Number) and isinstance(right, Number)):
            raise TypeError(f"Cannot divide {type(left).__name__} and {type(right).__name__}")
        if right.value == 0:
            print("Error: Division by zero")
            return None  # Instead of returning inf
        return Number(left.value / right.value)


    def visit_continue(self, node):
        raise ContinueSignal()

    def visit_modulo(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value % right.value)
        raise TypeError("Unsupported operands for modulo")

    def visit_power(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise TypeError("Power operator requires two numbers")

        return Number(left.value ** right.value)

    def visit_equals(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(abs(left.value - right.value) < 1e-9)
        if isinstance(left, Dict) and isinstance(right, Dict):
            return Boolean(left.elements == right.elements)
        if isinstance(left, List) and isinstance(right, List):
            if len(left.elements) != len(right.elements):
                return Boolean(False)
            for i in range(len(left.elements)):
                if not self.visit_equals(EqualsNode(left.elements[i], right.elements[i])).value:
                    return Boolean(False)
            return Boolean(True)

        if type(left) != type(right):
            return Boolean(False)
        return Boolean(left.value == right.value)
        
        # Original behavior for non-list types
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
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value < right.value)
        raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__} with <")

    def visit_greater_than(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value > right.value)
        raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__} with >")

    def visit_less_than_or_equal(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value <= right.value)
        raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__} with <=")

    def visit_greater_than_or_equal(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Number) and isinstance(right, Number):
            return Boolean(left.value >= right.value)
        raise TypeError(f"Cannot compare {type(left).__name__} and {type(right).__name__} with >=")

    def visit_and(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Boolean) and isinstance(right, Boolean):
            return Boolean(left.value and right.value)
        raise TypeError(f"Cannot perform AND on {type(left).__name__} and {type(right).__name__}")

    def visit_or(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        if isinstance(left, Boolean) and isinstance(right, Boolean):
            return Boolean(left.value or right.value)
        raise TypeError(f"Cannot perform OR on {type(left).__name__} and {type(right).__name__}")

    def visit_not(self, node):
        value = self.evaluate(node.node)
        if isinstance(value, Boolean):
            return Boolean(not value.value)
        raise TypeError(f"Cannot perform NOT on {type(value).__name__}")

    def visit_assign(self, node):
        try:
            value = self.evaluate(node.expression)
            if value is None:  # Happens on division by zero
                return None
            self.scopes[-1][node.identifier] = value
            return value
        except Exception as e:
            print(f"Error: {e}")
            return None

    def visit_print(self, node):
        value = self.evaluate(node.expression)
        print(value)  # ✅ Actually print it
        return value
  

    def visit_identifier(self, node):
        for scope in reversed(self.scopes):
            if node.identifier in scope:
                return scope[node.identifier]
        raise NameError(f"Variable '{node.identifier}' is not defined")

    def visit_if(self, node):
        condition = self.evaluate(node.condition)
        if not isinstance(condition, Boolean):
            raise TypeError("Condition in if statement must be boolean")

        if condition.value:
            for stmt in node.body:
                result = self.evaluate(stmt)
                if isinstance(result, ReturnException):
                    return result.value
        elif node.else_body:
            for stmt in node.else_body:
                result = self.evaluate(stmt)
                if isinstance(result, ReturnException):
                    return result.value
        return None



    def visit_while(self, node):
        while True:
            condition = self.evaluate(node.condition)
            if not isinstance(condition, Boolean):
                raise TypeError("Condition in while loop must be boolean")
            if not condition.value:
                break
            try:
                for stmt in node.body:
                    result = self.evaluate(stmt)
                    if isinstance(result, BreakSignal):
                        return None
                    elif isinstance(result, ContinueSignal):
                        break
                    elif isinstance(result, ReturnException):
                        return result.value
            except Exception as e:
                raise e
        return None
                    
   

    def visit_break(self, node):
        return BreakSignal()

    def visit_input(self, node):
        prompt = self.evaluate(node.prompt)
        if not isinstance(prompt, String):
            raise TypeError("Input prompt must be a string")
        user_input = input(prompt.value).strip()
        
        # Try to convert to number if possible
        try:
            if '.' in user_input:
                return Number(float(user_input))
            else:
                return Number(int(user_input))
        except ValueError:
            return String(user_input)

    # In Interpreter class
    def visit_index(self, node):
        container = self.evaluate(node.container)
        index = self.evaluate(node.index_expr)
        # If container is a list, expect a numeric index
        if isinstance(container, List):
            if not isinstance(index, Number):
                raise TypeError("List index must be a number")
            idx = int(index.value)
            if 0 <= idx < len(container.elements):
                return container.elements[idx]
            else:
                raise IndexError("List index out of range")
        # If container is a dict, expect a string/number/boolean key
        elif isinstance(container, Dict):
            if isinstance(index, (String, Number, Boolean)):
                key = index.value
            else:
                raise TypeError("Dictionary key must be string, number, or boolean")
            if key in container.elements:
                return container.elements[key]
            else:
                raise KeyError(f"Key '{key}' not found in dictionary")
        # For any other container type, indexing is not supported
        else:
            raise TypeError("Indexing is only supported for lists and dictionaries")







    # In Interpreter class
    def visit_dict_assign(self, node):
        container = self.evaluate(node.dict_expr)
        key_val = self.evaluate(node.key_expr)
        value = self.evaluate(node.value_expr)
        # Assign to dictionary
        if isinstance(container, Dict):
            if isinstance(key_val, (String, Number, Boolean)):
                key = key_val.value
            else:
                raise TypeError("Dictionary key must be string, number, or boolean")
            container.elements[key] = value  # set/update the dictionary entry
            return value
        # Assign to list index
        elif isinstance(container, List):
            if not isinstance(key_val, Number):
                raise TypeError("List index must be a number")
            idx = int(key_val.value)
            if idx < 0 or idx >= len(container.elements):
                raise IndexError("List index out of range")
            container.elements[idx] = value  # modify the list element in place
            return value
        # If the container is not a dict or list, it’s an invalid assignment target
        else:
            raise TypeError("Indexed assignment is only supported for lists and dictionaries")

            


    def visit_dict_access(self, node):
        dict_obj = self.evaluate(node.dict_expr)
        key = self.evaluate(node.key_expr)

        if not isinstance(dict_obj, Dict):
            raise Exception("Expected dictionary")

        if isinstance(key, (String, Number, Boolean)):
            key = key.value
        else:
            raise Exception("Dictionary key must be string, number, or boolean")

        if key not in dict_obj.elements:
            raise Exception(f"Key '{key}' not found in dictionary")

        return dict_obj.elements[key]

    def visit_function(self, node):
        closure_scope = self.scopes[-1].copy()  # Capture current scope
        self.functions[node.name] = {
            'parameters': node.parameters,
            'body': node.body,
            'closure': closure_scope  # Store closure
    }
        return None

    def visit_call(self, node):
        if node.name not in self.functions:
            raise NameError(f"Function '{node.name}' is not defined")
        func = self.functions[node.name]
        if len(node.arguments) != len(func["parameters"]):
            raise TypeError(f"Expected {len(func['parameters'])} arguments, got {len(node.arguments)}")
        
        evaluated_args = [self.evaluate(arg) for arg in node.arguments]
        new_scope = {**func["closure"], **dict(zip(func["parameters"], evaluated_args))}  # Merge closure scope
        self.scopes.append(new_scope)
        self.in_function = True
        
        try:
            result = None
            for stmt in func["body"]:
                result = self.evaluate(stmt)
                if isinstance(result, ReturnException):  # Handle return correctly
                    self.scopes.pop()
                    return result.value
            self.scopes.pop()
            return result
        except Exception as e:
            self.scopes.pop()
            raise e
        finally:
            self.in_function = False

    def visit_return(self, node):
        if not self.in_function:
            raise SyntaxError("Return statement outside of function")
        value = self.evaluate(node.value) if node.value else None
        raise ReturnException(value)
    
    def visit_is(self, node):
        left = self.evaluate(node.node_a)
        right = self.evaluate(node.node_b)
        
        if not isinstance(right, IdentifierNode):
            raise TypeError("Right side of 'is' must be a type identifier")
        
        type_map = {
            "Number": Number,
            "String": String,
            "Boolean": Boolean,
            "List": List,
            "Dict": Dict,
        }
        
        if right.identifier not in type_map:
            raise TypeError(f"Unknown type: {right.identifier}")
        
        expected_type = type_map[right.identifier]
        return Boolean(isinstance(left, expected_type))
    

    def visit_to_string(self, node):
        value = self.evaluate(node.expression)
        if isinstance(value, Number):
            if value.value.is_integer():
                return String(str(int(value.value)))
            return String(str(value.value))
        return String(str(value.value))
    
    def visit_list(self, node):
        evaluated_elements = []
        for element in node.elements:
            evaluated_elements.append(self.evaluate(element))
        return List(evaluated_elements)
    
    
    def visit_local_assign(self, node):
        value = self.evaluate(node.expression)
        self.scopes[-1][node.identifier] = value  # Store in current scope
        return value

    def evaluate(self, node):
        node_type = type(node)
        if node_type in self.visit_map:
            return self.visit_map[node_type](node)
        else:
            raise Exception(f"Unexpected node type: {node_type}")
        

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass


