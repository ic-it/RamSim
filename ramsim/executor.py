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
    callbacks: ICallbacks
    register: Register
    iostream: IIOstream
    pointer: Pointer
    path: str
    out: IOut

    def __init__(self, parsed_data: List[Operator], out: IOut, iostream: IIOstream, path: str, callbacks: ICallbacks = None) -> None:
        self.parsed_data = parsed_data
        self.callbacks = callbacks
        self.iostream = iostream
        self.register = Register()
        self.pointer = Pointer()
        self.path = path
        self.out = out

        # preprocessing
        if not self.includes() or not self.add_labels_to_pointer():
            self.parsed_data = []
            return
        
        # Pointer needs all lines amount
        self.pointer.max_line = len(self.parsed_data)-1
    
    def add_labels_to_pointer(self) -> bool:
        # Search for and add labels to the pointer. 
        # This seems to me to be the most convenient way to control the behavior of jumps 
        
        for n, op in enumerate(self.parsed_data):
            if not isinstance(op, LABEL):
                continue
            if not self.pointer.add_label(op.arg.data, n):
                self.out.runtime_error("Label is already exists", op.line, op.file_path)
                return False
        return True
        
    
    def includes(self) -> bool:
        # Loading other files specified in the code. 
        
        includes = []
        for n, op in enumerate(self.parsed_data):
            if not isinstance(op, INCLUDE):
                continue
        
            file_path = self.path + op.arg.data
            if not os.path.exists(file_path) and os.path.exists(file_path + ".ram"):
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
        # Execution of the code, it will execute infinitely. 
        # I have not yet figured out how to prevent infinite loops.
        while len(self.parsed_data):
            operator = self.parsed_data[self.pointer.line]

            if isinstance(operator, LABEL): ...
            if isinstance(operator, HALT):  break
            
            # Execute
            execute_error = operator.execute(self.register, self.pointer, self.iostream)
            
            # Pass the data to the callback. 
            # Data after execution
            if self.callbacks:
                self.callbacks.execute(self.register, operator, self.pointer)
            
            # Execute error processing
            if execute_error:
                self.out.runtime_error(execute_error, operator.line+1, operator.file_path)
                break

            # process register errors
            if self.register.has_errors():
                for error in self.register.get_errors():
                    self.out.runtime_error(error, operator.line+1, operator.file_path)
                break
            
            # Move pointer
            if not self.pointer.move():
                self.out.runtime_error("Use HALT to end the programm")
                break