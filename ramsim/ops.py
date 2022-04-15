from cProfile import label
from dataclasses import dataclass
from typing import Callable, List

from .pointer import Pointer
from .register import Register


@dataclass
class ArgI:
    data: int
    atype: int # 0 (Link)[]; 1 (No link)[=]; 2 (dLink)[*]

@dataclass
class ArgS:
    data: str

class Operator:
    arg: ArgI | ArgS
    tokens: List[str]
    line: int
    filename: str
    
    def execute(self, register: Register, pointer: Pointer):...

class OpI(Operator):
    arg: ArgI
    tokens: List[str] = None
    line: int
    filename: str

    def __init__(self, arg: ArgI, line: int, filename: str) -> None:
        self.arg = arg
        self.line = line
        self.filename = filename

    def __str__(self) -> str:
        return f"{self.tokens}: [{self.arg.data}; {self.arg.atype}]"

class OpS(Operator):
    arg: ArgS
    tokens: List[str]
    line: int
    filename: str

    def __init__(self, arg: ArgS, line: int, filename: str) -> None:
        self.arg = arg
        self.line = line
        self.filename = filename
    
    def __str__(self) -> str:
        return f"{self.tokens}: [{self.arg.data}]"

class AdditionalOp(Operator):
    arg: ArgS
    tokens: List[str]
    line: int
    filename: str

    def __init__(self, arg: ArgS, line: int, filename: str) -> None:
        self.arg = arg
        self.line = line
        self.filename = filename
    
    def __str__(self) -> str:
        return f"{self.tokens}: [{self.arg.data}]"


class LOAD(OpI):
    tokens: List[str] = ["LOAD", ]

    def execute(self, register: Register, pointer: Pointer):
        if self.arg.atype == 0:
            register.set(0, register.get(self.arg.data))
        if self.arg.atype == 1:
            register.set(0, self.arg.data)
        if self.arg.atype == 2:
            register.set(0, register.get(register.get(self.arg.data)))

class STORE(OpI):
    tokens: List[str] = ["STORE", ]

    def execute(self, register: Register, pointer: Pointer):
        if self.arg.atype == 0:
            register.set(self.arg.data, register.get(0))
        if self.arg.atype == 1:
            return "You cannot store number"
        if self.arg.atype == 2:
            register.set(register.get(self.arg.data), register.get(0))


# Math OPS
class MathOp:
    op_func: Callable

    def execute(self, register: Register, pointer: Pointer):
        if self.arg.atype == 0:
            register.set(0, self.op_func(register.get(0), register.get(self.arg.data)))
        if self.arg.atype == 1:
            register.set(0, self.op_func(register.get(0), self.arg.data))
        if self.arg.atype == 2:
            register.set(0, self.op_func(register.get(0), register.get(register.get(self.arg.data))))

class ADD(MathOp, OpI):
    tokens: List[str] = ["ADD", ]
    op_func: Callable = lambda s, a, b: a+b

class SUB(MathOp, OpI):
    tokens: List[str] = ["SUB", ]
    op_func: Callable = lambda s, a, b: a-b

class MUL(MathOp, OpI):
    tokens: List[str] = ["MUL", ]
    op_func: Callable = lambda s, a, b: a*b

class DIV(MathOp, OpI):
    tokens: List[str] = ["DIV", ]
    op_func: Callable = lambda s, a, b: a//b





class JMP(OpS):
    tokens: List[str] = ["JMP", "JUMP"]
    
    def execute(self, register: Register, pointer: Pointer):
        if not pointer.move_to_label(self.arg.data):
            return f"Label '{self.arg.data}' not found"

class JZ(OpS):
    tokens: List[str] = ["JZ", "JUMP_ZERO"]

    def execute(self, register: Register, pointer: Pointer):
        if register.get(0) != 0:
            return
        if not pointer.move_to_label(self.arg.data):
            return f"Label '{self.arg.data}' not found"

class JGZ(OpS):
    tokens: List[str] = ["JGZ", ]
    
    def execute(self, register: Register, pointer: Pointer):
        if register.get(0) > 0:
            return
        if not pointer.move_to_label(self.arg.data):
            return f"Label '{self.arg.data}' not found"

class LABEL(OpS):
    tokens: List[str] = ["/LABEL", ]

class HALT:
    tokens: List[str] = ["HALT", ]
    line: int
    filename: str

    def __init__(self, line: int, filename: str) -> None:
        self.line = line
        self.filename = filename
            
    __str__ = lambda self: "[HALT]"


class INCLUDE(AdditionalOp):
    tokens: List[str] = ["INCLUDE", ]


class PRINT(AdditionalOp):
    tokens: List[str] = ["PRINT", ]
    
    def execute(self, register: Register, pointer: Pointer):
        
        if self.arg.data.isdigit():
            print(register.get(int(self.arg.data)))
        elif self.arg.data.startswith("*") and self.arg.data[1:].isdigit():
            print(register.get(register.get(int(self.arg.data[1:]))))
        else:
            print(self.arg.data)


ops: List[OpS | OpI] = [
    LOAD,
    STORE,
    ADD,
    SUB,
    MUL,
    DIV,
    JMP,
    JZ,
    JGZ,
    HALT,

    INCLUDE,
    PRINT
]