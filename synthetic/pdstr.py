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
        
        self._update_state(string)
        self.raw += string
        
        return AppendResult(
            code=AppendResultCode.OK,
            state=self._state
            )
        
    def complete (self) -> bool :
        if self._complete: return True
        
        ends_with_end_tag = re.compile(r"<END>(\s*)$")
        if ends_with_end_tag.search(self.raw) :
            self._complete = True
            return True
        return False
            
    def stop_sequences (self) -> List[str] :
        stop_sequences = []
        if self.is_start() :
            stop_sequences += ["<HEAD>"]
        elif self.is_head() :
            stop_sequences += ["</HEAD>"]
        elif self.is_middle(): 
            stop_sequences += ["<START>"]
        elif self.is_body() :
            stop_sequences += ["<END>"]
        else :
            stop_sequences += [""]
            
        return stop_sequences
    
    def is_start (self) -> bool :
        self._set_state()
        return self._state.location == Location.START
    
    def is_middle (self) -> bool :
        self._set_state()
        return self._state.location == Location.MIDDLE
    
    def is_end (self) -> bool :
        self._set_state()
        return self._state.location == Location.END
    
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
        
    def _update_state(self, string: str) -> None :
        if self._state is None :
            raise ValueError("Can not update the state of a pdstr if is None, must use _set_state instead.")
        
        self._state.update(string)        
    