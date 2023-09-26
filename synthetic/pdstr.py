import re
from typing import List, Optional, Tuple
from warnings import warn

from .pdstr_append_result import AppendResult, AppendResultCode
from .dynamic_state import DynamicState, Location
from .validators import ValidationCode, ValidatorSet
from .validators.default import PDSTR_DEFAULT_VALIDATOR_SET
class PartialDynamicString () :
    raw: str
    validation_set: ValidatorSet
    
    _state: Optional[DynamicState] = None
    _complete: bool = False
    
    def __init__(self, string: str, validator_set: ValidatorSet = PDSTR_DEFAULT_VALIDATOR_SET) -> None :
        code, string = validator_set.validate(string)
        if code == ValidationCode.WARN :
            warn(f"Validator had to update string.")
        elif code == ValidationCode.FAIL :
            raise ValueError("The string must follow the desired format to pass validation.")
        
        self.raw = string
        self._set_state()
        self.validation_set = validator_set
        
        
    def append(self, string: str) -> AppendResult :
        
        concatenated_string = self.raw + string
        
        code, concatenated_string = self.validation_set.validate(concatenated_string)
        
        if code == ValidationCode.FAIL :
            return AppendResult(code=AppendResultCode.ERROR)
        
        
        self._update_state(string)
        self.raw += string
        
        code = AppendResultCode.OK if code == ValidationCode.OK else AppendResult.WARN
        
        return AppendResult(
            code=code,
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
            stop_sequences += ["<END>", ")->"]
        else :
            stop_sequences += [""]
            
        return stop_sequences
    
    def get_fcall (self) -> Tuple[str, str] :
        if not self.is_fcalling():
            raise ValueError("Can not extract function call if pdstr is not calling a function.")
    
        extract_function_call = re.compile(r"\[(.*)\((.*)\)->$", flags=re.M)
        match = extract_function_call.search(self.raw)
        
        if not match :
            raise RuntimeError("Regular expression did not match")
        
        return match.groups()
        
         
    
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
    
    def is_fcalling (self) -> bool :
        self._set_state()
        return self._state.is_function_calling
         
    def _set_state(self) -> None :
        if self._state is None :
            self._state = DynamicState(self.raw)
        
    def _update_state(self, string: str) -> None :
        if self._state is None :
            raise ValueError("Can not update the state of a pdstr if is None, must use _set_state instead.")
        
        self._state.update(string)        
    