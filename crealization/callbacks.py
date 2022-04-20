import os
from pprint import pprint
from typing import List
from ramsim.icallbacks import ICallbacks
from ramsim.pointer import Pointer
from ramsim.register import Register
from ramsim.ops import Operator

class Callbacks(ICallbacks):
    def __init__(self, break_points: List[int], main_file: str) -> None:
        self.break_points = break_points if break_points else []
        self.main_file = os.path.abspath(main_file)
    
    def execute(self, register: Register, operator: Operator, pointer: Pointer):
        if operator.line+1 not in self.break_points or os.path.abspath(operator.file_path) != self.main_file:
            return
        print("Operator:")
        print("\tLine:", operator.line+1)
        print("\tOperator:", operator)
        print("Register:")
        print("\t", register.register)
        input("Continue?:")
        print("\n\n\n")