from typing import Union
from typing import List, Optional
from .iiostream import IIOstream


class CIOstream(IIOstream):
    def __init__(self, inp: List[int] = None, out: List[int] = None) -> None:
        if not out:
            out = []
        
        self.inp = inp
        self.out = out
    
    def input(self) -> Union[int, None]:
        if self.inp:
            return self.inp.pop(0)
        
        i = input("Input: ")
        return int(i) if i.isdigit() else None
    
    def output(self, value: int) -> None:
        self.out.append(value)
        print(value)