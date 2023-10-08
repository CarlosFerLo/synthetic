from typing import Protocol

class FunctionCall (Protocol) :
    """Base type for the callable property of a Function
    """
    def __call__(input: str) -> str :
        pass

class Function () :
    """Base class for functions
    """
    name: str
    description: str
    func: FunctionCall
    
    def __init__ (self, name: str, description: str, func: FunctionCall) -> None:
        self.name = name
        self.description = description
        self.func = func