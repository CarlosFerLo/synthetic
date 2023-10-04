from synthetic import AppendResult

class String () :
    raw: str
    
    def __init__ (self, string: str) -> None :
        self.raw = string
        
    def __add__ (self, string: str) -> AppendResult :
        self.raw += string
        return AppendResult()