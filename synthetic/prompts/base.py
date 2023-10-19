from typing import List, Any, Optional

import synthetic

class PromptTemplate () :
    """Base class for prompt templates
    
    Properties:
        template (str): template that will be formatted
        input_variables (List[str]): input variable names (must all appear in the template)
        
    Methods:
        format (**kwargs: Any) -> str: formats template by changing {var_name} for its value  
    """
    template: str
    input_variables: List[str]
    
    def __init__(self, template: str, input_variables: List[str], prefix: Optional[str] = None) -> None:
        self.validate(template=template, input_variables=input_variables, prefix=prefix)
        
        self.template = template
        self.input_variables = input_variables
        self.prefix = prefix
        
    def format(self, **kwargs: Any) -> str :
        if kwargs.keys() != set(self.input_variables) :
            raise synthetic.PromptTemplateError(f"Input must be {self.input_variables} and it is {list(kwargs.keys())}")
        try:
            prompt = self.template.format(**kwargs)
        except KeyError as e :
            raise synthetic.PromptTemplateError(e)
        
        if self.prefix is not None :
            prompt = self.prefix + prompt
        
        return prompt
    
    def validate(self, template:str, input_variables: List[str], prefix: Optional[str] = None) -> None:
        for var in input_variables :
            if template.find("{" + var + "}") == -1 :
                raise synthetic.PromptTemplateError(f"The input variable '{var}' should appear in the template.")
        