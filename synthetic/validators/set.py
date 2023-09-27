from typing import List, Tuple

from .base import Validator, ValidationCode

class ValidatorSet ():
    validators: List[Validator]
    
    def __init__ (self, validators: List[Validator]) -> None:
        self.validators = validators
        
    def validate (self, string: str) -> Tuple[ValidationCode, str]:
        code = ValidationCode.OK
        for validator in self.validators :
            new_code, string = validator.validate(string)
            
            if new_code == ValidationCode.WARN :
                code = new_code
            elif new_code == ValidationCode.FAIL :
                return (new_code, string)
            
        return (code, string)