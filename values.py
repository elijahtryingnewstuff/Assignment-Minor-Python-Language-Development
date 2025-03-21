from dataclasses import dataclass

class String:
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("String value must be a string")
        self.value = value

    def __repr__(self):
        return f'"{self.value}"'


@dataclass
class Number:
    value: any

    def __repr__(self):
        return f"{self.value}"

@dataclass
class Boolean:
    value: bool

    def __repr__(self):
        return "true" if self.value else "false"