from .pointer import Pointer
from .register import Register
from .ops import Operator

class ICallbacks:
    def execute(self, register: Register, operator: Operator, pointer: Pointer): ...