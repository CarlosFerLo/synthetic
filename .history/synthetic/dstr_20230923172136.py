from .dstrdict import DynamicStringDict, DictElement

from .utils.dstr_validation import VALIDATORS
from .utils.dstr_to_dict import get_head_and_body

class DynamicString ():
    raw: str
    
    def __init__ (self, string: str) -> None :
        if not self._validate_str(string) :
            raise ValueError("The string must follow the desired format to pass validation.")
        
        self.raw = string
        
    def as_dict (self) -> DynamicStringDict :
        head, body = get_head_and_body(self.raw)
        
        return DynamicStringDict(head, body)
        
    def _validate_str (self, string: str) -> bool :
        string = string.strip()
        
        for v in VALIDATORS :
            if not v(string) :
                return False
        
        return True
        
        
        
        
        
    

    
    