import os
from pprint import pprint
from time import sleep
from typing import List

from .icallbacks import ICallbacks
from .register import Register
from .ops import HALT, LABEL, Operator, INCLUDE
from .pointer import Pointer
from .iout import IOut
from .iiostream import IIOstream
from .parser import Parser

class Executor:
    parsed_data: List[Operator]
    pointer: Pointer

    def __init__(self, parsed_data: List[Operator], out: IOut, iostream: IIOstream, register: Register, path: str, callbacks: ICallbacks = None) -> None:
        self.parsed_data = parsed_data
        self.out = out
        self.register = register
        self.pointer = Pointer(len(self.parsed_data)-1)
        self.path = path
        self.iostream = iostream
        self.callbacks = callbacks

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
                self.out.runtime_error("Label is already exists", op.line, op.file_path)
                return False
        return True
        
    
    def includes(self) -> bool:
        includes = []
        for n, op in enumerate(self.parsed_data):
            if not isinstance(op, INCLUDE):
                continue
        
            file_path = self.path + op.arg.data
            if not file_path.endswith(".ram"):
                file_path += ".ram"
            if not os.path.exists(file_path):
                self.out.runtime_error(f"File {file_path} not exists", op.line, op.file_path)
                return False
            p = Parser(file_path, self.out)
            self.parsed_data.pop(n)
            if not p.parse():
                return False
            includes += p.parsed_data
        self.parsed_data = includes + self.parsed_data
        return True
    
    def execute(self) -> bool:
        while len(self.parsed_data):
            line = self.pointer.line
            operator = self.parsed_data[line]
            if isinstance(operator, LABEL):
                ...
            if isinstance(operator, HALT):
                break

            operator_error = operator.execute(self.register, self.pointer, self.iostream)
            if self.callbacks:
                self.callbacks.execute(self.register, operator, self.pointer)
            
            if operator_error:
                self.out.runtime_error(operator_error, operator.line+1, operator.file_path)
                break
            if self.register.has_errors():
                for error in self.register.get_errors():
                    self.out.runtime_error(error, operator.line+1, operator.file_path)
                break
            if not self.pointer.move():
                self.out.runtime_error("Use HALT to end the programm")
                break