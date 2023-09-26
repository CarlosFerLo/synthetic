from typing import Optional

from .pdstr import PartialDynamicString
from .dstrdict import DynamicStringDict

from synthetic.utils.dstr_to_dict import get_head_and_body
from .validators import ValidatorSet, ValidationCode
from.validators.default import DSTR_DEFAULT_VALIDATOR_SET

class DynamicString ():
    raw: str
    validation_set: ValidatorSet
    
    def __init__ (self, 
                  string: Optional[str] = None, 
                  pdstring: Optional[PartialDynamicString] = None,
                  validation_set: ValidatorSet = DSTR_DEFAULT_VALIDATOR_SET
    ) -> None :
        if string and pdstring : raise ValueError("Can not initiate a dstr from both a string and a pdstr.")
        if not string and not pdstring : raise ValueError("Need to provide a string or pdstr to init a dstr.")
        
        self.validation_set = validation_set
        
        if string :
            code, string = self.validation_set.validate(string)
            if code == ValidationCode.FAIL :
                raise ValueError("The string must follow the desired format to pass validation.")
            elif code == ValidationCode.WARN :
                raise Warning("The input string failed some tests but it was solved.")
            self.raw = string
   
        elif pdstring :
            if not pdstring.complete() :
                raise ValueError("Can not instatiate a dstr from an incomplete pdstr")
            
            self.raw = pdstring.raw
    
    def as_dict (self) -> DynamicStringDict :
        head, body = get_head_and_body(self.raw)
        
        return DynamicStringDict(head=head, body=body)    
    
        
        
        
        
        
    

    
    