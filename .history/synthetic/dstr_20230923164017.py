from typing import List, Callable

from .utils.dstr_validation import str_has_head_body_structure

VALIDATORS: List[Callable[[str], bool]]

class DynamicString ():
    raw: str
    
    def __init__ (self, string: str) -> None :
        if not self._validate_str(string) :
            raise ValueError("The string must follow the desired format to pass validation.")
        
        self.raw = string
        
    def _validate_str (self, string: str) -> bool :
        string = string.strip()
        
        for v in VALIDATORS :
            if not v(string) :
                return False
        
        return True
        
        
        
        
        
    

    
    