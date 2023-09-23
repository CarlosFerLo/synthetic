from typing import Callable

from .functiondict import FunctionDict

InferenceFunction = Callable[[FunctionDict], FunctionDict]
    

class Function ():
    name: str
    description: str
    inference: InferenceFunction
    
    