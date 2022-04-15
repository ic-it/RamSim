from .iout import IOut


class Out(IOut):
    def __init__(self) -> None:
        pass
    
    def runtime_error(self, text: str, line: int = None, filename: str = None):
        print(f"Runtime error%s%s:" % (f" on line {line}"if line else "", f" in file {filename}" if filename else ""), text)
    
    def syntax_error(self, text: str, line: int, filename: str):
        print(f"Syntax error on line {line} in {filename}:", text)