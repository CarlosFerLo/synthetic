from typing import List

from synthetic.llms import LLM
from synthetic.prompts import PromptTemplate
from synthetic.functions import Function

class Agent () :
    """ Agent class for synthetic.
    """
    llm: LLM
    prompt_template: PromptTemplate
    functions: List[Function]
    
    def __init__(self, 
                 llm: LLM,
                 prompt_template: PromptTemplate, 
                 functions: List[Function] = []
        ) -> None:
        self.llm = llm
        self.prompt_template = prompt_template
        self.functions = functions