from typing import Dict, Optional

class FunctionDict ():
    dict: Dict[str, str]
    input_tag: str
    output_tag: str
    
    def __init__ (self, dict: Dict[str, str],
        input_tag: str = "input", output_tag: str = "output"
    ) -> None :
        self.dict = dict
        self.input_tag = input_tag
        self.output_tag = output_tag
        
        if not self.input_tag in dict.keys() and not self.output_tag in dict.keys():
            raise ValueError("Need to include the input or output tag in the FunctionDict")