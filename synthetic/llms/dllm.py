from typing import List
from langchain.llms.base import LLM

from synthetic import dstr, pdstr, AppendResultCode, DynamicState, Location

from .generation_error import GenerationError
from synthetic.functions import Function

class DynamicLLM ():
    llm: LLM
    prefix: str
    functions: List[Function]
    
    max_iter: int
    
    def __init__(self, llm: LLM, max_iter: int = 5, prefix: str = "", functions: List[Function] = []) -> None:
        self.llm = llm
        self.max_iter = max_iter
        self.prefix = prefix
        self.functions = functions
        
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
            
            if result.state.location == Location.START :
                pdstring.append("<HEAD>")
            elif result.state.location == Location.MIDDLE :
                pdstring.append("<START>")
                
            if result.state.is_function_calling :
                name, input = pdstring.get_fcall()
                
                for f in self.functions :
                    if f.name == name :
                        output = f(input)
                
                pdstring.append(output + "]")
            
            if pdstring.complete():
                return dstr(pdstring=pdstring)
            
        raise GenerationError("max_iteration limit was reached")
    
    def build_prompt (self, prompt: str) -> str :        
        return self.prefix + prompt