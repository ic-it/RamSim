import os

from typing import List, Tuple, Union
from .ops import HALT, AdditionalOp, ops, LABEL, ArgS, ArgI, OpS, OpI
from .iout import IOut

class Parser:
    parsed_data: List[Union[HALT, OpI, OpS, AdditionalOp]]
    out: IOut
    file_path: str


    def __init__(self, file_path: str, out: IOut) -> None:        
        self.parsed_data: List[Union[HALT, OpI, OpS, AdditionalOp]] = []
        self.out = out
        self.file_path = file_path
        self.read_data_from_file()

    def read_data_from_file(self):
        if not os.path.exists(self.file_path):
            self.out.syntax_error("File not exists", -1, self.file_path)
            self.file_path = None
            return False
            
        with open(self.file_path, 'r') as f:
            file_data = f.read()
        
        if '\n' in file_data:
            self.input_value = file_data.split("\n")
        else:
            self.input_value = file_data
        
        return True

    def parse(self) -> bool:
        "Go line by line"

        if not self.file_path:
            return False
        for linen, line in enumerate(self.input_value):
            status, message = self.parse_line(line, linen)
            if not status:
                self.out.syntax_error(message, linen + 1, self.file_path)
                return False
        return True
    
    def get_token(self, line: str):
        "Looks for a token at the beginning of a string, if it finds one, but gives a search status of False"
        
        token_found = False     # whether the token is found
        ftoken = ""             # found token
        fop = None              # found operator

        for op in ops:
            for token in op.tokens:
                if not line.startswith(token) and not line.startswith(token.lower()): 
                    continue
                if not ftoken:
                    ftoken, fop, token_found = token, op, True
                    continue
                if len(token) > len(ftoken):
                    ftoken, fop, token_found = token, op, True
                    continue
        
        # split line
        # in theory, you can write without spaces, but I don't recommend it.
        line = line[len(ftoken):]
        return token_found, line, fop
    
    @staticmethod
    def clear_start_and_end(string: str):
        "removing spaces or tabs in start and end"

        while string.startswith(" ") or string.startswith("\t"):
            string = string[1:]
        while string.endswith(" ") or string.endswith("\t"):
            string = string[:-1]
        return string

    def parse_line(self, line: str, linen: int) -> Tuple[bool, str]:

        # clear comments
        if line.startswith("#"):
            return True, ""
        while "#" in line:
            line, _ = line.split("#", 1)

        line = self.clear_start_and_end(line)

        # if after cleaning, the string is empty, then ignore
        if not line:
            return True, ""
        
        # if is label
        if line.endswith(":"):
            # clear label
            line = line[:-1]
            line = self.clear_start_and_end(line)

            # If there is a space inside the label, there is a mistake )
            if "\t" in line or " " in line:
                return False, "Incorrect label syntax"
            self.parsed_data.append(LABEL(ArgS(line), linen, self.file_path))
            return True, ""
        
        # Find operator
        token_found, line, op = self.get_token(line)

        if not token_found:
            return False, "Incorrect token"
        
        if issubclass(op, OpI):
            # If an operator requires an int type argument, it can have a constant(=), a direct() and a double(*) reference. 
            # The characters before a number determine which type is passed to the operator
            # Everything else is basically clear
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
        
        if issubclass(op, OpS):
            # Here, if the operator requires a string, we must clear the string and add it to the arguments
            op: OpS

            line = line.replace(' ', '').replace('\'', '').replace('"', '')
            self.parsed_data.append(op(ArgS(line), linen, self.file_path))
            return True, ""
        
        if issubclass(op, AdditionalOp):
            # Additional operators, they all require a stopper
            op: AdditionalOp

            line = line.replace(" ", "")
            self.parsed_data.append(op(ArgS(line), linen, self.file_path))
            return True, ""
        
        if issubclass(op, HALT):
            # HALT \_(-._.-)_/

            self.parsed_data.append(op(linen, self.file_path))
            return True, ""
        
        # TODO In general, the correct way is to rewrite it so that it is added not by type of operator, but by its argument type, but.... 
        # TODO Sometime later
        return False, "?ERROR?"