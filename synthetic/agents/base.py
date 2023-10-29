from typing import List, Type

from .agent_output import AgentOutput, FunctionCall

import synthetic.re as re
from synthetic.llms import LLM
from synthetic.prompts import PromptTemplate
from synthetic.functions import Function
from synthetic.errors import InvalidSignatureError, InvalidFunctionNameError
from synthetic.components import Component

class Agent () :
    """ Agent class for synthetic.
    """
    llm: LLM
    prompt_template: PromptTemplate
    functions: List[Function]
    components: List[Type[Component]]
    
    signature: str
    signature_pattern: re.Pattern
    partial_signature: str
    partial_signature_pattern: re.Pattern
    function_output_suffix: str
      
    def __init__(self, 
                 llm: LLM,
                 prompt_template: PromptTemplate, 
                 functions: List[Function] = [],
                 signature: str = "[{name}({input})->{output}]",
                 components: List[Type[Component]] = []
        ) -> None:
        self.llm = llm
        self.prompt_template = prompt_template
        self.functions = functions
        
        self._validate_signature(signature)
        self.signature = signature
        self.signature_pattern = re.compile(signature, key_pattern_dict={ "name": r"(\S*)" })
        
        self.partial_signature, self.function_output_suffix = signature.split("{output}")
        self.partial_signature_pattern = re.compile(self.partial_signature + "$", key_pattern_dict={ "name": r"(\S*)"}, flags = re.M)
        
        dynamic_components, static_components = [], []
        for c in components :
            (static_components, dynamic_components)[c.is_dynamic].append(c)
            
        self.components = dynamic_components
        self.prompt_template.add_components(static_components)
        
        
    def call(self, max_iters: int = 10, **kwargs) -> AgentOutput :
        prompt = self.prompt_template.format(**dict(kwargs, **self.__dict__))
        generation = ""
        
        for _ in range(0, max_iters) :
            stop = self._stop_sequences()
            gen = self.llm(
                prompt=prompt,
                stop=stop
            )
            
            generation += gen
            prompt += gen
            
            if not any([ re.search(s, prompt) for s in stop]) :
                break
                
            m = re.search(self.partial_signature_pattern, prompt)
            if m :
                function_called = False
                for function in self.functions:
                    if function.name == m["name"]:
                        output = function(input = m["input"])
                        function_called = True
                        break
                if not function_called:
                    raise InvalidFunctionNameError(f"No function with name: {m['name']}")
                
                generation += output + self.function_output_suffix
                prompt += output + self.function_output_suffix
            
        return AgentOutput(
            generation=generation,
            raw=prompt,
            function_calls=self._get_function_calls(prompt)
        )
        
    def _validate_signature (self, signature: str) -> None :
        required_elements = ["{name}" , "{input}", "{output}"]
        if not all(element in signature for element in required_elements):
            raise InvalidSignatureError("Signature must include {name}, {input}, and {output} in this order.")
        for i in range(len(required_elements) - 1):
            if signature.index(required_elements[i]) > signature.index(required_elements[i + 1]):
                raise InvalidSignatureError("Elements in signature must be in the order: {name}, {input}, {output}.")

    def _stop_sequences (self) -> List[str | re.Pattern] :
        return [ self.partial_signature_pattern.pattern ]
    
    def _get_function_calls (self, string: str) -> List[FunctionCall] :
        matches = re.findall(self.signature_pattern, string)
        return [
            FunctionCall(
                name=m["name"],
                input=m["input"],
                output=m["output"]
            ) for m in matches
        ]