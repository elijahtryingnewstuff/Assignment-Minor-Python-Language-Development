from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    NUMBER    = 0
    PLUS      = 1
    MINUS     = 2
    MULTIPLY  = 3
    DIVIDE    = 4
    LPAREN    = 5
    RPAREN    = 6
    TRUE      = 7
    FALSE     = 8
    EQUALS    = 9
    NOTEQUAL  = 10
    LESS      = 11
    GREATER   = 12
    LESSEQ    = 13
    GREATEREQ = 14
    AND       = 15
    OR        = 16
    NOT       = 17
    POW       = 18
    STRING    = 19
    IDENTIFIER = 20
    PRINT     = 21

@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value is not None else "")