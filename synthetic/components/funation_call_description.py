from typing import Any
from .base import Component

class FunctionCallDescription (Component) :
    name = "FunctionCallDescription"
    def format(self, **kwargs: Any) -> str:
        signature = kwargs["signature"]
        
        return signature