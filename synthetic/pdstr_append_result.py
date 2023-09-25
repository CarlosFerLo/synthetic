from enum import Enum
from typing import Optional

from .dynamic_state import DynamicState

AppendResultCode = Enum("AppenResultCode", ["OK", "ERROR"])

class AppendResult () :
    code: AppendResultCode
    state: Optional[DynamicState]
    
    def __init__(self, 
                 state: Optional[DynamicState] = None,
                 code: AppendResultCode = AppendResultCode.OK
    ) -> None:
        self.code = code
        self.state = state
