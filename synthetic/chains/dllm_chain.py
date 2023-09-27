from typing import Any
from langchain.prompts import PromptTemplate

from synthetic.llms import DynamicLLM

class DynamicLLMChain () :
    dllm: DynamicLLM
    prompt_template: PromptTemplate
    
    def __init__(self, dllm: DynamicLLM, prompt_template: PromptTemplate) -> None:
        self.dllm = dllm
        self.prompt_template = prompt_template
        
        
    def format(self, **kwargs: Any) -> str :
        return self.prompt_template.format(**kwargs)