import re
from typing import List, Optional

from .utils.pdstr_validators import PDSTR_VALIDATORS
from .pdstr_append_result import AppendResult, AppendResultCode
from .dynamic_state import DynamicState, Location

class PartialDynamicString () :
    raw: str
    
    _state: Optional[DynamicState] = None
    _complete: bool = False
    
    def __init__(self, string: str) -> None :
        if not self._validate_str(string) :
            raise ValueError("The string must follow the desired format to pass validation.")
        
        self.raw = string
        self._set_state()
        
        
    def append(self, string: str) -> AppendResult :
        
        concatenated_string = self.raw + string
        
        print(concatenated_string)
        
        if not self._validate_str(concatenated_string) :
            return AppendResult(code=AppendResultCode.ERROR)
        
        self.raw += string
        
        return AppendResult(code=AppendResultCode.OK)
        
    def complete (self) -> bool :
        if self._complete: return True
        
        ends_with_end_tag = re.compile(r"<END>(\s*)$")
        if ends_with_end_tag.search(self.raw) :
            self._complete = True
            return True
        return False
            
    def stop_sequences (self) -> List[str] :
        stop_sequences = []
        if self.is_head() :
            stop_sequences += ["</HEAD>"]
            
        return stop_sequences
    
    def is_head (self) -> bool :
        self._set_state()
        return self._state.location == Location.HEAD
    
    def is_body (self) -> bool :
        self._set_state()
        return self._state.location == Location.BODY
    
    def _validate_str(self, string: str) -> bool :
        string = string.strip()
        
        for v in PDSTR_VALIDATORS :
            if not v(string) :
                return False
        
        return True
         
    def _set_state(self) -> None :
        if self._state is None :
            self._state = DynamicState(self.raw)
        
    
            
    