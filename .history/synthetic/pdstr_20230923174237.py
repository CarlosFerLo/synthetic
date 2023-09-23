from .utils.pdstr_validators import PDSTR_VALIDATORS

class PartialDynamicString () :
    raw: str
    
    def __init__(self, string: str) -> None :
        if not self._validate_str(string) :
            raise ValueError("The string must follow the desired format to pass validation.")
        
        self.raw = string
        
    def _validate_str(self, string: str) -> bool :
        string = string.strip()
        
        for v in PDSTR_VALIDATORS :
            if not v(string) :
                return False
        
        return True
         