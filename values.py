from dataclasses import dataclass

@dataclass
class String:
    value: str
    def __repr__(self):
        return f'"{self.value}"'

@dataclass
class Number:
    value: float
    def __repr__(self):
        if self.value == float('inf'):
            return "inf"
        if self.value.is_integer():
            return str(int(self.value))
        return str(self.value)

@dataclass
class Boolean:
    value: bool
    def __repr__(self):
        return "true" if self.value else "false"
    
@dataclass
class List:
    elements: list
    def __repr__(self):
        return "[" + ", ".join(map(repr, self.elements)) + "]"
    
@dataclass
class Dict:
    elements: dict
    def __init__(self, elements=None):
        self.elements = elements if elements is not None else {}
    def __repr__(self):
        if not self.elements:
            return "{}"
        items = []
        for k, v in self.elements.items():
            if isinstance(k, str):
                k_repr = f'"{k}"'
            else:
                k_repr = str(k)
            items.append(f"{k_repr}: {v}")
        return "{" + ", ".join(items) + "}"
    
@dataclass
class ReturnValue:
    value: any

class BreakSignal:
    pass

class ContinueSignal:
    pass