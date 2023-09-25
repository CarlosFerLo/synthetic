from typing import Any
from langchain.llms.base import LLM

from synthetic import dstr, pdstr, AppendResultCode

from .generation_error import GenerationError

class DynamicLLM ():
    llm: LLM
    prefix: str
    
    max_iter: int
    
    def __init__(self, llm: LLM, max_iter: int = 5, prefix: str = "") -> None:
        self.llm = llm
        self.max_iter = max_iter
        self.prefix = prefix
        
    def __call__(self, pdstring: pdstr) -> dstr:
        for _ in range(self.max_iter) :
            stop_sequences = pdstring.stop_sequences()
            output = self.llm(
                prompt=self.build_prompt(pdstring.raw),
                stop=stop_sequences
            )
            
            result = pdstring.append(output)
            
            if result.code == AppendResultCode.ERROR :
                raise GenerationError("ERROR code returned when appending generation to pdstr.")
            
            if pdstring.complete():
                return dstr(pdstring=pdstring)
            
        raise GenerationError("max_iteration limit was reached")
    
    def build_prompt (self, prompt: str) -> str :
        return self.prefix + prompt