from enum import Enum

AppendResultCode = Enum("AppenResultCode", ["OK", "ERROR"])

class AppendResult () :
    code: AppendResultCode
    
    def __init__(self, code: AppendResultCode = AppendResultCode.OK) -> None:
        self.code = code
