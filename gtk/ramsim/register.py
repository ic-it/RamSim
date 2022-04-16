from typing import Dict, List
from .iout import IOut

class Register:
    register: Dict[int, int]
    errors: List[str]

    def __init__(self) -> None:
        self.register = {0: 0}
        self.errors = []
    
    def get_errors(self):
        while self.errors:
            yield self.errors.pop(0)
    
    def get(self, i: int) -> int | None:
        if i not in self.register:
            self.errors.append(f"You cannot get {i} register")
            return
        return self.register[i]
    
    def set(self, i: int, v: int) -> bool:
        if i < 0:
            self.errors.append(f"You cannot set {i} register")
            return False
        self.register[i] = v
        return True