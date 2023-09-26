from typing import Callable

class Function ():
    name: str
    description: str
    call: Callable[[str], str]
    
    def __init__ (self, name: str, description: str, call: Callable[[str], str]) :
        self.name = name
        self.description = description
        self.call = call
        
    def __call__(self, string: str) -> str:
        return self.call(string)
    
    def describe (self) -> str:
        return f"{self.name}: {self.description}"