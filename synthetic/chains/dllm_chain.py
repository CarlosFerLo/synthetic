from typing import Any
from langchain.prompts import PromptTemplate

from synthetic import dstr, pdstr
from synthetic.llms import DynamicLLM

class DynamicLLMChain () :
    dllm: DynamicLLM
    prompt_template: PromptTemplate
    
    def __init__(self, dllm: DynamicLLM, prompt_template: PromptTemplate) -> None:
        try :
            pdstr(prompt_template.template)
        except :
            raise ValueError("PromptTemplate can not be converted to pdstr.")
        
        self.dllm = dllm
        self.prompt_template = prompt_template
        
        
    def format(self, **kwargs: Any) -> str :
        return self.prompt_template.format(**kwargs)
    
    def run(self, **kwargs: Any) -> dstr :
        prompt = self.format(**kwargs)
        pdstring=pdstr(prompt)
        return self.dllm(pdstring)