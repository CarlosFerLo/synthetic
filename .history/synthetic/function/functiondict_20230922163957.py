from typing import Dict, Optional

class FunctionDict ():
    dict: Dict[str, str]
    input_tag: str = "input"
    output_tag: str = "output"
    
    def __init__ (self, dict: Dict[str, str],
        input_tag: Optional[str], output_tag: Optional[str]
    ) -> None :
        self.dict = dict
        
        if input_tag : self.input_tag = input_tag
        if output_tag: self.output_tag=output_tag
        
        if not self.input_tag in dict.keys() and not self.output_tag in dict.keys():
            raise ValueError("Need to include the input or output tag in the function Dict")