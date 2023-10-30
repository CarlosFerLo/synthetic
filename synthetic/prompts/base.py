from typing import List, Any, Type

import synthetic
import synthetic.re as re
from synthetic.components import Component, load_components

class PromptTemplate () :
    """Base class for prompt templates
    
    Properties:
        template (str): template that will be formatted
        input_variables (List[str]): input variable names (must all appear in the template)
        
        components(List[Type[Component]]): components that are expected in the prompt template
        
    Methods:
        format (**kwargs: Any) -> str: formats template by changing {var_name} for its value  
    """
    template: str
    input_variables: List[str]
    
    components: List[Type[Component]]
    
    def __init__(self, template: str, input_variables: List[str], components: List[Type[Component]] = []) -> None:
        self.validate(template=template, input_variables=input_variables, components=components)
        
        self.template = template
        self.input_variables = input_variables
        
        standard_components = load_components(template)
        standard_components = [ s for s in standard_components if all([ s.name != c.name for c in components ]) ]
        
        self.components = components + standard_components
        
    def add_components(self, components: List[Type[Component]]) -> None :
        self._validate_components(components=self.components+components)
        self.components += components
        
    def format(self, **kwargs: Any) -> str :
        if kwargs.keys() < set(self.input_variables) :
            raise synthetic.PromptTemplateError(f"Input must be {self.input_variables} and it is {list(kwargs.keys())}")
        try:
            prompt = self.template.format(**kwargs)
        except KeyError as e :
            raise synthetic.PromptTemplateError(e)
        
        for comp in self.components :
            signature = comp.signature()
            matches = re.findall(signature, prompt)
            for m in matches :
                inst = comp(**m)
                try :
                    string = inst.format(**kwargs)
                except TypeError as e :
                    raise synthetic.PromptTemplateError(e)
                prompt = prompt.replace(m["match"], string, 1)
            
        return prompt
    
    @classmethod
    def validate(cls, template:str, input_variables: List[str], components: List[Type[Component]] = []) -> None:
        cls._validate_input_variables_appear_in_template(template=template, input_variables=input_variables)
        cls._validate_components(components=components)    
        
    @staticmethod
    def _validate_input_variables_appear_in_template (template: str, input_variables: List[str]) -> None :
       for var in input_variables :
            if template.find("{" + var + "}") == -1 :
                raise synthetic.PromptTemplateError(f"The input variable '{var}' should appear in the template.")
         
    @staticmethod
    def _validate_components (components: List[Type[Component]]) -> None :
        component_names = [component.name for component in components]
        if len(component_names) != len(set(component_names)):
            raise synthetic.ComponentConflictError("Two components cannot have the same name.")
        
        dynamic_components = [ c for c in components if c.is_dynamic ]
        if len(dynamic_components) > 0 :    
            raise synthetic.DynamicComponentInPromptTemplateError(f"Dynamic components are not allowed in PromptTemplate. Dynamic components: {dynamic_components}.")
