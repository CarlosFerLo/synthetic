from enum import Enum

class AppendResultCode (Enum, int):
    OK = 0

class AppendResult () :
    code: AppendResultCode
    
    def __init__(self, code: AppendResultCode = AppendResultCode.OK) -> None:
        self.code = code
