from .utils.pdstr_validators import PDSTR_VALIDATORS
from .pdstr_append_result import AppendResult, AppendResultCode

class PartialDynamicString () :
    raw: str
    
    def __init__(self, string: str) -> None :
        if not self._validate_str(string) :
            raise ValueError("The string must follow the desired format to pass validation.")
        
        self.raw = string
        
    def append(self, string: str) -> AppendResult :
        
        concatenated_string = self.raw + string
        
        print(concatenated_string)
        
        if not self._validate_str(concatenated_string) :
            return AppendResult(code=AppendResultCode.ERROR)
        
        self.raw += string
        
        return AppendResult(code=AppendResultCode.OK)
        
    def _validate_str(self, string: str) -> bool :
        string = string.strip()
        
        for v in PDSTR_VALIDATORS :
            if not v(string) :
                return False
        
        return True
         