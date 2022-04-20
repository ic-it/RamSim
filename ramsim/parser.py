from ctypes import Union
from re import L
from typing import List, Tuple, TextIO
from .ops import HALT, AdditionalOp, ops, LABEL, ArgS, ArgI, OpS, OpI
from .iout import IOut

class Parser:
    def __init__(self, file_path: str, out: IOut) -> None:
        with open(file_path, 'r') as f:
            self.input_value = f.read().split("\n")
        self.parsed_data: List[Union[HALT, OpI, OpS, AdditionalOp]] = []
        self.out = out
        self.file_path = file_path
    
    def parse(self) -> bool:
        for linen, line in enumerate(self.input_value):
            status, message = self.parse_line(line, linen)
            if not status:
                self.out.syntax_error(message, linen + 1, self.file_path)
                return False
        return True
    
    def get_token(self, line: str):
        tokenisf = False
        ftoken = ""
        fop = None
        for op in ops:
            for token in op.tokens:
                if line.startswith(token) or line.startswith(token.lower()): 
                    if not ftoken:
                        ftoken, fop, tokenisf = token, op, True
                        continue
                    if len(token) > len(ftoken):
                        ftoken, fop, tokenisf = token, op, True
                        continue
        line = line[len(ftoken):]
        return tokenisf, line, fop

    def parse_line(self, line: str, linen: int) -> Tuple[bool, str]:

        # clear
        if line.startswith("#"):
            return True, ""
        while "#" in line:
            line, _ = line.split("#", 1)
        #

        # remove spaces in start and end
        while line.startswith(" ") or line.startswith("\t"):
            line = line[1:]
        while line.endswith(" ") or line.startswith("\t"):
            line = line[:-1]
        #

        # if line is empty
        if not line:
            return True, ""
        # 
        
        # LABEL syntx "asdasd:"
        if line.endswith(":"):
            line = line[:-1]
            self.parsed_data.append(LABEL(ArgS(line), linen, self.file_path))
            return True, ""
        
        # Find operator
        token_found, line, op = self.get_token(line)

        if not token_found:
            return False, "Incorrect token"
        
        if issubclass(op, OpI):
            op: OpI

            atype = 0
            if "=" in line:
                atype = 1
                line = line.replace("=", "", 1)
            if "*" in line:
                atype = 2
                line = line.replace("*", "", 1)
            line = line.replace(" ", "")

            if not line.isdigit():
                return False, "Incorrect args"
            self.parsed_data.append(op(ArgI(int(line), atype), linen, self.file_path))
            return True, ""
        elif issubclass(op, OpS):
            op: OpS

            line = line.replace(' ', '').replace('\'', '').replace('"', '')
            self.parsed_data.append(op(ArgS(line), linen, self.file_path))
            return True, ""
        elif issubclass(op, AdditionalOp):
            op: AdditionalOp

            line = line.replace(" ", "")
            self.parsed_data.append(op(ArgS(line), linen, self.file_path))
            return True, ""
        elif issubclass(op, HALT):
            self.parsed_data.append(op(linen, self.file_path))
            return True, ""
        return False, "?ERROR?"