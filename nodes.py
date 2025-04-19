from dataclasses import dataclass

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
class UnaryOpNode:
    operator: any
    node: any

@dataclass
class AssignNode:
    identifier: str
    expression: any

@dataclass
class PrintNode:
    expression: any

@dataclass
class IdentifierNode:
    identifier: str