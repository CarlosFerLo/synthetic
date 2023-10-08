from typing import List, Any

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
    
    def __init__(self, template: str, input_variables: List[str]) -> None:
        for var in input_variables :
            if template.find("{" + var + "}") == -1 :
                raise synthetic.PromptTemplateError(f"The input variable '{var}' should appear in the template.")
        
        self.template = template
        self.input_variables = input_variables
        
    def format(self, **kwargs: Any) -> str :
        if kwargs.keys() != set(self.input_variables) :
            raise synthetic.PromptTemplateError(f"Input must be {self.input_variables} and it is {list(kwargs.keys())}")
        try:
            prompt = self.template.format(**kwargs)
        except KeyError as e :
            raise synthetic.PromptTemplateError(e)
        return prompt