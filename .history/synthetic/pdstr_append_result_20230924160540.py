from enum import Enum

class AppendResultCode (Enum, int):
    OK = "0"

class AppendResult () :
    code: AppendResultCode
