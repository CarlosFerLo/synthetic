class DynamicString ():
    raw: str
    
    def __init__ (self, string: str) -> None :
        if not self._validate_str(string) :
            raise ValueError("The string must follow the desired format to pass validation.")
        
        self.raw = string