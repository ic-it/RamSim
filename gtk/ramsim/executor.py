from typing import List

from .register import Register
from .ops import HALT, AdditionalOp, ops, LABEL, ArgS, ArgI, OpS, OpI, Operator, INCLUDE
from .pointer import Pointer
from .iout import IOut
from .parser import Parser

class Executor:
    parsed_data: List[Operator]
    pointer: Pointer

    def __init__(self, parsed_data: List[Operator], out: IOut, register) -> None:
        self.parsed_data = parsed_data
        self.out = out
        self.register = register
        self.pointer = Pointer(len(self.parsed_data)-1)

        # preprocessing
        if not self.includes() or not self.add_labels_to_pointer():
            return
        
        # Pointer needs all lines amount
        self.pointer.max_line = len(self.parsed_data)-1
    
    def add_labels_to_pointer(self) -> bool:
        for n, op in enumerate(self.parsed_data):
            if not isinstance(op, LABEL):
                continue
            if not self.pointer.add_label(op.arg.data, n):
                self.out.runtime_error("Label is already exists", op.line, op.filename)
                return False
        return True
        
    
    def includes(self):
        includes = []
        for n, op in enumerate(self.parsed_data):
            if not isinstance(op, INCLUDE):
                continue
        
            file_path = op.arg.data
            if not file_path.endswith(".ram"):
                op.arg.data += ".ram"
            with open(op.arg.data, "r") as f:
                p = Parser(f, self.out)
            self.parsed_data.pop(n)
            if not p.parse():
                return False
            includes += p.parsed_data
        self.parsed_data = includes + self.parsed_data
        return True
    
    def execute(self):
        while True:
            line = self.pointer.line
            operator = self.parsed_data[line]
            if isinstance(operator, LABEL):
                ...
            if isinstance(operator, HALT):
                break

            operator_error = operator.execute(self.register, self.pointer)
            if operator_error:
                self.out.runtime_error(operator_error, operator.line+1, operator.filename)
                break
            for error in self.register.get_errors():
                self.out.runtime_error(error, operator.line+1, operator.filename)
                break
            if not self.pointer.move():
                self.out.runtime_error("Use HALT to end the programm")
                break