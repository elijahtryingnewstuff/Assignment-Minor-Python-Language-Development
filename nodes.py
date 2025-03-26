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
    condition: any
    true_block: any
    false_block: any = None
    def __repr__(self):
        return f"IfNode(condition={self.condition}, true_block={self.true_block}, false_block={self.false_block})"

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

    