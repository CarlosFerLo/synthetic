from typing import Callable

class Function ():
    name: str
    description: str
    call: Callable[[str], str]