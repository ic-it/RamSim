

class IOut:
    def syntax_error(self, text: str, line: int , filename: str):...
    def runtime_error(self, text: str, line: int = None, filename: str = None):...

    