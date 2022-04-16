from typing import Dict
from .iout import IOut

class Pointer:
    line: int
    max_line: int
    labels: Dict[str, int]
    error: str

    def __init__(self, max_line: int) -> None:
        self.line = 0
        self.max_line = max_line
        self.labels = {}
        self.error = ""
    
    def move(self, line: int = None) -> bool:
        if not line:
            line = self.line + 1
        if line < 0 or line > self.max_line:
            return False
        self.line = line
        return True
    
    def move_to_label(self, label: str) -> bool:
        if not label in self.labels:
            return False
        self.line = self.labels[label]
        return True
    
    def add_label(self, label: str, line: int) -> bool:
        if label in self.labels:
            return False
        self.labels[label] = line
        return True
