from dataclasses import dataclass

class StatementsNode:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"StatementsNode({self.statements})"

@dataclass
class StringNode:
    value: str
    def __repr__(self):
        return f'"{self.value}"'

@dataclass
class NumberNode:
    value: any
    def __repr__(self):
        return f"{self.value}"

@dataclass
class BooleanNode:
    value: bool
    def __repr__(self):
        return "true" if self.value else "false"

@dataclass
class AddNode:
    node_a: any
    node_b: any

@dataclass
class SubtractNode:
    node_a: any
    node_b: any

@dataclass
class MultiplyNode:
    node_a: any
    node_b: any

@dataclass
class DivideNode:
    node_a: any
    node_b: any

@dataclass
class EqualsNode:
    node_a: any
    node_b: any

@dataclass
class NotEqualsNode:
    node_a: any
    node_b: any

@dataclass
class LessThanNode:
    node_a: any
    node_b: any

@dataclass
class GreaterThanNode:
    node_a: any
    node_b: any

@dataclass
class LessThanOrEqualNode:
    node_a: any
    node_b: any

@dataclass
class GreaterThanOrEqualNode:
    node_a: any
    node_b: any

@dataclass
class AndNode:
    node_a: any
    node_b: any

@dataclass
class OrNode:
    node_a: any
    node_b: any

@dataclass
class NotNode:
    node: any

@dataclass
class PowerNode:
    node_a: any
    node_b: any

@dataclass
class AssignNode:
    identifier: str
    expression: any

@dataclass
class PrintNode:
    expression: any
    def __repr__(self):
        return f"print({self.expression})" 

@dataclass
class IdentifierNode:
    identifier: str

@dataclass
class IfNode:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body      # ✅ list of statements inside if
        self.else_body = else_body  # ✅ optional list of statements inside else


@dataclass
class WhileNode:
    condition: any
    body: any
    def __repr__(self):
        return f"WhileNode(condition={self.condition}, body={self.body})"

@dataclass
class BreakNode:
    def __repr__(self):
        return "BreakNode()"

@dataclass
class InputNode:
    prompt: any
    def __repr__(self):
        return f"InputNode(prompt={self.prompt})"

@dataclass
class ModuloNode:
    node_a: any
    node_b: any

@dataclass
class ListNode:
    elements: list  
    def __repr__(self):
        return f"List({self.elements})"

@dataclass
class IndexNode:
    container: any
    index_expr: any
    def __repr__(self):
        return f"{self.container}[{self.index_expr}]"

    
@dataclass
class DictNode:
    elements: dict
    def __repr__(self):
        return "{" + ", ".join(f"{k}:{v}" for k,v in self.elements.items()) + "}"

@dataclass
class DictAccessNode:
    dict_expr: any
    key_expr: any
    def __repr__(self):
        return f"{self.dict_expr}[{self.key_expr}]"
    
    
@dataclass
class FunctionNode:
    name: str
    parameters: list[str]
    body: list

@dataclass
class ReturnNode:
    value: any

@dataclass
class CallNode:
    name: str
    arguments: list


@dataclass
class IsNode:
    node_a: any
    node_b: any

@dataclass
class ToStringNode:
    expression: any

class ListAssignNode:
    def __init__(self, list_expr, index_expr, value_expr):
        self.list_expr = list_expr
        self.index_expr = index_expr
        self.value_expr = value_expr
    
@dataclass
class DictAssignNode:
    dict_expr: any
    key_expr: any
    value_expr: any
    is_local: bool = False

@dataclass
class ContinueNode:
    pass

@dataclass
class ListAssignNode:
    list_expr: any
    index_expr: any
    value_expr: any