from typing import List

import synthetic.re as re
from synthetic.llms import LLM
from synthetic.prompts import PromptTemplate
from synthetic.functions import Function
from synthetic.errors import InvalidSignatureError

class Agent () :
    """ Agent class for synthetic.
    """
    llm: LLM
    prompt_template: PromptTemplate
    functions: List[Function]
    signature: str
      
    def __init__(self, 
                 llm: LLM,
                 prompt_template: PromptTemplate, 
                 functions: List[Function] = [],
                 signature: str = "[{name}({input})->{output}]"
        ) -> None:
        self.llm = llm
        self.prompt_template = prompt_template
        self.functions = functions
        
        self._validate_signature(signature)
        self.signature = signature
        self.signature_pattern = re.compile(signature, key_pattern_dict={ "name": "(\S*)" })
        self.partial_signature = signature.split("{output}")[0]
        self.partial_signature_pattern = re.compile(self.partial_signature, key_pattern_dict={ "name": "(\S*)"})
        
    def _validate_signature (self, signature: str) -> None :
        required_elements = ["{name}" , "{input}", "{output}"]
        if not all(element in signature for element in required_elements):
            raise InvalidSignatureError("Signature must include {name}, {input}, and {output} in this order.")
        for i in range(len(required_elements) - 1):
            if signature.index(required_elements[i]) > signature.index(required_elements[i + 1]):
                raise InvalidSignatureError("Elements in signature must be in the order: {name}, {input}, {output}.")
