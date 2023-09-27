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
    describe_functions: bool
    
    def __init__(self, 
                 llm: LLM, 
                 max_iter: int = 5, 
                 prefix: str = "",
                 sufix: str = "",
                 functions: List[Function] = [],
                 describe_functions: bool = True,
                 verbosity: bool = False
    ) -> None:
        self.llm = llm
        self.max_iter = max_iter
        self.prefix = prefix
        self.sufix = sufix
        self.functions = functions
        self.describe_functions = describe_functions
        self.verbosity = verbosity
        
    def __call__(self, pdstring: pdstr) -> dstr:
        if self.verbosity: print(self.build_prompt(pdstring.raw))
        for _ in range(self.max_iter) :
            stop_sequences = pdstring.stop_sequences()
            output = self.llm(
                prompt=self.build_prompt(pdstring.raw),
                stop=stop_sequences
            )
            result = pdstring.append(output)
            if self.verbosity: print(f"{result.code}: {output}")
            if result.code == AppendResultCode.ERROR :
                raise GenerationError(f"ERROR code returned when appending generation to pdstr.\n{pdstring.raw}{output}")
            
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
        describe_functions = "\n".join(map(lambda x: x.describe(), self.functions)) if self.describe_functions else ""   
        return self.prefix + describe_functions + self.sufix + prompt