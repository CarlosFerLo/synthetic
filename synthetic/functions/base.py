from typing import Any, Protocol

class FunctionCallable (Protocol) :
    """Base type for the callable property of a Function
    """
    def __call__(input: str) -> str :
        pass

class Function () :
    """Base class for functions
    """
    name: str
    description: str
    func: FunctionCallable
    
    def __init__ (self, name: str, description: str, func: FunctionCallable) -> None:
        self.name = name
        self.description = description
        self.func = func
        
    def __call__(self, input: str) -> Any:
        return self.func(input)