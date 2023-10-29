from typing import Any, List

import synthetic.re as re

class Component () :
    name: str = "Component"
    is_dynamic: bool = False
    
    id: str
    
    _idx: int = 0
    
    def __new__(cls, **kwargs) -> "Component":
        cls._idx += 1
        
        return super(Component, cls).__new__(cls)
        
    def __init__ (self, **kwargs) -> None :
        self.id = f"{self.name}-{self._idx}"
        
    def format (self, **kwargs: Any) -> str :
        raise NotImplementedError("Format method is not implemented by base component class.")
        
    @classmethod
    def signature(cls) :
        return re.compile("<" + cls.name + "/>")
    
    @classmethod
    def _reset_idx(cls) :
        cls._idx = 0