from cProfile import label
from dataclasses import dataclass
from typing import Callable, List

from .iiostream import IIOstream
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
    file_path: str
    
    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):...

class OpI(Operator):
    arg: ArgI
    tokens: List[str] = None
    line: int
    file_path: str

    def __init__(self, arg: ArgI, line: int, file_path: str) -> None:
        self.arg = arg
        self.line = line
        self.file_path = file_path

    def __str__(self) -> str:
        return f"{self.tokens}: [{self.arg.data}; {self.arg.atype}]"

class OpS(Operator):
    arg: ArgS
    tokens: List[str]
    line: int
    file_path: str

    def __init__(self, arg: ArgS, line: int, file_path: str) -> None:
        self.arg = arg
        self.line = line
        self.file_path = file_path
    
    def __str__(self) -> str:
        return f"{self.tokens}: [{self.arg.data}]"

class AdditionalOp(Operator):
    arg: ArgS
    tokens: List[str]
    line: int
    file_path: str

    def __init__(self, arg: ArgS, line: int, file_path: str) -> None:
        self.arg = arg
        self.line = line
        self.file_path = file_path
    
    def __str__(self) -> str:
        return f"{self.tokens}: [{self.arg.data}]"


class LOAD(OpI):
    tokens: List[str] = ["LOAD", ]

    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        if self.arg.atype == 0:
            register.set(0, register.get(self.arg.data))
        if self.arg.atype == 1:
            register.set(0, self.arg.data)
        if self.arg.atype == 2:
            register.set(0, register.get(register.get(self.arg.data)))

class STORE(OpI):
    tokens: List[str] = ["STORE", ]

    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        if self.arg.atype == 0:
            register.set(self.arg.data, register.get(0))
        if self.arg.atype == 1:
            return "You cannot store number"
        if self.arg.atype == 2:
            register.set(register.get(self.arg.data), register.get(0))

class WRITE(OpI):
    tokens: List[str] = ["WRITE", ]

    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        value = None
        if self.arg.atype == 0:
            value = register.get(self.arg.data)
        if self.arg.atype == 1:
            value = self.arg.data
        if self.arg.atype == 2:
            value = register.get(register.get(self.arg.data))
        if value:
            iostream.output(value)

class READ(OpI):
    tokens: List[str] = ["READ", ]

    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        value = iostream.input()
        if self.arg.atype == 0:
            register.set(self.arg.data, value)
        if self.arg.atype == 1:
            return "You cannot store number"
        if self.arg.atype == 2:
            register.set(register.get(self.arg.data), value)

# Math OPS
class MathOp:
    op_func: Callable

    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        r0 = register.get(0)
        rx = None
        if self.arg.atype == 0:
            rx = register.get(self.arg.data)
        if self.arg.atype == 1:
            rx = self.arg.data
        if self.arg.atype == 2:
            rx = register.get(register.get(self.arg.data))
        if None in [r0, rx]:
            return
        register.set(0, self.op_func(r0, rx))

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
    
    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        if not pointer.move_to_label(self.arg.data):
            return f"Label '{self.arg.data}' not found"

class JZ(OpS):
    tokens: List[str] = ["JZ", "JUMP_ZERO"]

    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        if register.get(0) != 0:
            return
        if not pointer.move_to_label(self.arg.data):
            return f"Label '{self.arg.data}' not found"

class JGZ(OpS):
    tokens: List[str] = ["JGZ", ]
    
    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        if register.get(0) > 0:
            return
        if not pointer.move_to_label(self.arg.data):
            return f"Label '{self.arg.data}' not found"

class LABEL(OpS):
    tokens: List[str] = ["/LABEL", ]

class HALT:
    tokens: List[str] = ["HALT", ]
    line: int
    file_path: str

    def __init__(self, line: int, file_path: str) -> None:
        self.line = line
        self.file_path = file_path
            
    __str__ = lambda self: "[HALT]"


class INCLUDE(AdditionalOp):
    tokens: List[str] = ["INCLUDE", ]


class PRINT(AdditionalOp):
    tokens: List[str] = ["PRINT", ]
    
    def execute(self, register: Register, pointer: Pointer, iostream: IIOstream):
        
        if self.arg.data.isdigit():
            print(register.get(int(self.arg.data)))
        elif self.arg.data.startswith("*") and self.arg.data[1:].isdigit():
            print(register.get(register.get(int(self.arg.data[1:]))))
        else:
            print(self.arg.data)


ops: List[OpS | OpI] = [
    LOAD,
    STORE,
    WRITE,
    READ,
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