from typing import Callable, Tuple, Optional
from enum import Enum

ValidationCode = Enum("Validation Code", ["OK", "WARN", "FAIL"])

class Validator () :
    test: Callable[[str], bool]
    resolve: Optional[Callable[[str], str]] = None
    
    def __init__ (self, test: Callable[[str], str], resolve: Optional[Callable[[str], str]] = None) -> None:
        self.test = test
        self.resolve = resolve

    def validate (self, string: str) -> Tuple[ValidationCode, str]:
        if self.test(string):
            return (ValidationCode.OK, string)
        if not self.resolve :
            return (ValidationCode.FAIL, string)
        
        try :
            new_str = self.resolve(string)
            return (ValidationCode.WARN, new_str)
        except :
            return (ValidationCode.FAIL, string)
        
    