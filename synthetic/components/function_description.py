from typing import Any, List

from synthetic.functions import Function

from .base import Component

class FunctionDescriptions (Component) :
    """ Standard component for function description
    """
    name = "FunctionDescriptions"
    
    def format(self, **kwargs: Any) -> str:
        functions: List[Function] = kwargs["functions"]
        
        return "\n".join([ f"-{f.name}: {f.description}" for f in functions ])