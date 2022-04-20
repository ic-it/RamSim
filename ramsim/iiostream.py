from typing import Union
from typing import Optional


class IIOstream:
    def input(self) -> Union[int, None]:...
    def output(self, value: int) -> None:...