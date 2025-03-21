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
        return f"{self.value}"

@dataclass
class Boolean:
    value: bool

    def __repr__(self):
        return "true" if self.value else "false"