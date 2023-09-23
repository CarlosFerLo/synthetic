import re

from .utils.dstr_validation import str_has_head_body_structure

class DynamicString ():
    raw: str
    
    def __init__ (self, string: str) -> None :
        if not self._validate_str(string) :
            raise ValueError("The string must follow the desired format to pass validation.")
        
        self.raw = string
        
    def _validate_str (self, string: str) -> bool :
        string = string.strip()
        
        if not str_has_head_body_structure(string) :
            return False
        
        return True
        
        
        
        
        
    

    
    