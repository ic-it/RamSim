from typing import Union
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
    
    def has_errors(self) -> bool:
        return True if len(self.errors) else False
    
    def get(self, i: int) -> Union[int, None]:
        if i not in self.register:
            self.errors.append(f"You cannot get register {i}")
            return
        return self.register[i]
    
    def set(self, i: int, v: int) -> bool:
        if i < 0 or not isinstance(i, int):
            self.errors.append(f"You cannot set register {i}")
            return False
        self.register[i] = v
        return True
    
    def __str__(self) -> str:
        return str(self.register)