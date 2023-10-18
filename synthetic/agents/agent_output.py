from dataclasses import dataclass
from typing import List

@dataclass
class FunctionCall () :
    name: str
    input: str
    output: str

@dataclass
class AgentOutput () :
    generation: str
    raw: str
    function_calls: List[FunctionCall]