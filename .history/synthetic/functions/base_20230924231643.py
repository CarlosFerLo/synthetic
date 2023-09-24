from typing import Callable

class Function ():
    name: str
    description: str
    call: Callable[[str], str]
    
    def __init__ (self, name: str, description: str, call: Callable[[str], str]) :
        self.name = name
        self.description = description
        self.call = call