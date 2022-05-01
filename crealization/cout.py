from ramsim.iout import IOut


class COut(IOut):
    def __init__(self) -> None:
        pass
    
    def runtime_error(self, text: str, line: int = None, file_path: str = None):
        print(f"Runtime error%s%s:" % (f" on line {line}"if line else "", f" in file {file_path}" if file_path else ""), text)
    
    def syntax_error(self, text: str, line: int, file_path: str):
        print(f"Syntax error on line {line} in {file_path}:", text)