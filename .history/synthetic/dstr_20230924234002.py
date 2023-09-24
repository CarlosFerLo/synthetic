from typing import Optional

from .pdstr import PartialDynamicString
from .dstrdict import DynamicStringDict

from .utils.dstr_validation import DSTR_VALIDATORS
from .utils.dstr_to_dict import get_head_and_body

class DynamicString ():
    raw: str
    
    def __init__ (self, string: Optional[str], pdstring: Optional[PartialDynamicString]) -> None :
        if string and pdstring : raise ValueError("Can not initiate a dstr from both a string and a pdstr.")
        if not string and not pdstring : raise ValueError("Need to provide a string or pdstr to init a dstr.")
        
        if string :
            if not self._validate_str(string) :
                raise ValueError("The string must follow the desired format to pass validation.")
            
            self.raw = string
   
        elif pdstring :
            if not pdstring.complete() :
                raise ValueError("Can not instatiate a dstr from an incomplete pdstr")
            
            self.raw = pdstring.raw
    
    def as_dict (self) -> DynamicStringDict :
        head, body = get_head_and_body(self.raw)
        
        return DynamicStringDict(head=head, body=body)
        
    def _validate_str (self, string: str) -> bool :
        string = string.strip()
        
        for v in DSTR_VALIDATORS :
            if not v(string) :
                return False
        
        return True
        
        
        
        
        
    

    
    